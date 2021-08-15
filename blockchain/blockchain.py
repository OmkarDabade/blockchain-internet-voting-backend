from hashlib import sha1
from database.adminModel import Admin
from database.voterModel import Voter
from database.candidateModel import Candidate
from block.vote import Vote
from constants import *
import requests
from datetime import datetime
from flask import request
from database import voterDb, adminDb, candidateDb


class Blockchain:
    """
    Blockchain class to store votes
    """

    def __init__(self):
        self.previousIndex: int = 0
        self.previousHash: str = GENESIS_BLOCKHASH
        self.chain: list[Vote] = []

    def addBlock(self, candidateId: int, candidateName: str, voterId: str):
        """
        A function that adds the vote data to the chain.
        """
        print("Adding Block to chain")

        if len(self.chain) == 0:
            newBlock = Vote(
                0,
                candidateId,
                candidateName,
                sha1(voterId.encode()).hexdigest(),
                datetime.now(),
                GENESIS_BLOCKHASH,
            )

            self.chain.append(newBlock)
            self.previousHash = newBlock.blockHash
        else:
            newBlock = Vote(
                self.previousIndex + 1,
                candidateId,
                candidateName,
                sha1(voterId.encode()).hexdigest(),
                datetime.now(),
                self.previousHash,
            )

            self.chain.append(newBlock)
            self.previousIndex += 1
            self.previousHash = newBlock.blockHash

        self.announceNewBlock(newBlock)

        if self.previousIndex % CONSENSOUS_AFTER_N_BLOCKS == 0:
            self.consensus()

    def acceptNewAnnouncedBlock(self, block: Vote):
        """
        A function that adds the newly announced block to the chain after verification.
        """
        print("Accept New Anounced Block")

        print("Previous     HASH:", self.previousHash)
        print("Recived BlockHASH:", block.previousBlockHash)

        if self.previousHash != block.previousBlockHash:
            print("Hash doesnt match")
            return False

        if not self.isValidProof(block, block.blockHash):
            print("is not valid proof")
            return False

        print("Block added to chain")
        self.chain.append(block)
        self.previousIndex += 1
        self.previousHash = block.blockHash
        return True

    @classmethod
    def isValidProof(cls, block: Vote, blockHash: str):
        """
        Check if blockHash is valid hash of block and satisfies the difficulty criteria.
        """
        return (
            blockHash.startswith("0" * BLOCKCHAIN_DIFFICULTY)
            and blockHash == block.computeHash()
        )

    @classmethod
    def isChainValid(cls, chainDump: dict):
        """
        Check if chain satisfies validity criteria ie block should give given hash and that
        hash should be linked to previous block
        """
        result = True
        previousHash = GENESIS_BLOCKHASH

        for blockData in chainDump:
            block = Vote.fromJson(blockData)

            if (
                not cls.isValidProof(block, block.blockHash)
                or previousHash != block.previousBlockHash
            ):
                result = False
                break
            previousHash = block.blockHash

        return result

    def syncChain(self, chainDump: dict):
        """
        Completely replace current chain with new valid chain
        """
        res = self.isChainValid(chainDump)
        if res:
            newChain: list[Vote] = []

            for voteData in chainDump:
                vote = Vote.fromJson(voteData)
                newChain.append(vote)

            self.chain = newChain
            self.previousIndex = self.chain[-1].index
            self.previousHash = self.chain[-1].blockHash
            print("Successfully synced the chain")
        else:
            print("Chain is tampered unable to sync")

        return res

    def announceNewBlock(self, block: Vote):
        """
        A function to announce to the network once a block has been mined.
        Other blocks can simply verify the proof of work and add it to their
        respective chains.
        """
        print("Annoucing New Block To Peers")

        if len(peers) == 0:
            print("no registered peers, returning...")
            return

        for peer in peers:
            url = "{}addBlock".format(peer)

            res = requests.post(url=url, json=block.toJson(), headers=POST_HEADERS)
            print("Peer: ", peer)
            print("API Response: ", res.text)

    def getChainInJson(self):
        """
        Get chain in JSON format
        """
        chain = []
        for vote in self.chain:
            chain.append(vote.toJson())

        return chain

    def consensus(self):
        """
        Consensus Algorithm:
        If a longer valid chain is found, our chain is replaced with it.
        """
        print("Consensous called")

        if len(peers) == 0:
            print("No registerd peers, returning...")
            return

        print("CURRENT NODE ADDRESS: ", request.host_url)

        # Peers
        # -----------------------------------------------------------------------------

        print("Getting All Peers")
        longestPeerList = None
        currentPeerLength = len(peers)

        # Check for longest peer list
        for node in peers:
            response = requests.get("{}syncPeers".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentPeerLength:
                longestPeerList = jsonData["peers"]
                currentPeerLength = jsonData["length"]

        # If there is no longestPeerList then we sync current list with all nodes
        if longestPeerList == None:
            longestPeerList = list(peers)
            currentPeerLength = len(peers)

        # If longer peer list than current peer list is avialable sync it with current node
        if len(longestPeerList) != len(peers):
            for peer in longestPeerList:
                if request.host_url != peer:
                    peers.add(str(peer))

        newPeers: list = list(peers)
        newPeers.append(request.host_url)

        currentPeerLength = len(peers)
        print("Syncing Peers with other nodes")

        # Sync longest peer list among all nodes
        for node in peers:
            response = requests.get("{}syncPeers".format(node))
            jsonData = response.json()
            if jsonData["length"] != currentPeerLength:
                resp = requests.post(
                    url="{}syncPeers".format(node),
                    json={"peers": newPeers},
                    headers=POST_HEADERS,
                )
                if resp.status_code != 200:
                    print("Unable to Sync Peers with Node:", node)

        # Chain
        # -----------------------------------------------------------------------------

        print("Getting Chain")
        longestValidChainDump = None
        currentChainLength = len(self.chain)

        # Check for longest chain
        for node in peers:
            response = requests.get("{}syncChain".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentChainLength and self.isChainValid(
                jsonData["chain"]
            ):
                longestValidChainDump = jsonData["chain"]
                currentChainLength = jsonData["length"]

        # If there is no longestValidChainDump then we sync current chain with all nodes
        if longestValidChainDump == None:
            longestValidChainDump = self.getChainInJson()
            currentChainLength = len(self.chain)

        # If longest valid chain avialable sync it with current node
        if len(longestValidChainDump) != len(self.chain):
            self.syncChain(longestValidChainDump)

        # longestPeerList = None
        currentChainLength = len(self.chain)
        print("Syncing chain with other nodes")

        # Sync longest valid chain among all nodes
        for node in peers:
            response = requests.get("{}syncChain".format(node))
            jsonData = response.json()

            if jsonData["length"] != currentChainLength or not self.isChainValid(
                jsonData["chain"]
            ):
                resp = requests.post(
                    url="{}syncChain".format(node),
                    json={"chain": self.getChainInJson()},
                    headers=POST_HEADERS,
                )
                if resp.status_code != 200:
                    print("Unable to Sync Chain with Node:", node)

        # Candidates
        # -----------------------------------------------------------------------------

        print("Getting Candidates")
        longestCandidateData = None
        currentCandidateDataLength = candidateDb.totalCandidates()

        # Check for longest candidate list
        for node in peers:
            response = requests.get("{}syncCandidates".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentCandidateDataLength:
                longestCandidateData = jsonData["candidates"]
                currentCandidateDataLength = jsonData["length"]

        # If there is no longestCandidateData then we sync current list with all nodes
        if longestCandidateData == None:
            longestCandidateData = candidateDb.getAllCandidatesInJson()
            currentCandidateDataLength = candidateDb.totalCandidates()

        allCandidatesInCurrentNode = candidateDb.allCandidates()

        # If longest candidate list avialable sync it with current node
        if len(longestCandidateData) != candidateDb.totalCandidates():
            for candidateData in longestCandidateData:
                candidate = Candidate.fromJson(candidateData)
                if candidate.candidateId not in allCandidatesInCurrentNode:
                    candidateDb.addCandidate(
                        candidate.candidateId,
                        candidate.candidateName,
                        candidate.state,
                        candidate.district,
                        candidate.ward,
                    )

        currentCandidateDataLength = candidateDb.totalCandidates()
        print("Syncing Candidates with other nodes")

        # Sync longest candidate list among all nodes
        for node in peers:
            response = requests.get("{}syncCandidates".format(node))
            jsonData = response.json()
            if jsonData["length"] != currentCandidateDataLength:
                resp = requests.post(
                    url="{}syncCandidates".format(node),
                    json={"candidates": candidateDb.getAllCandidatesInJson()},
                    headers=POST_HEADERS,
                )
                if resp.status_code != 200:
                    print("Unable to Sync Canidates with Node:", node)

        # Voter Database
        # -----------------------------------------------------------------------------

        print("Getting Voter Database")
        largestVoterDatabase = None
        currentVoterDatabaseLength = voterDb.totalVoters()

        # Check if largest voterDb is avialable
        for node in peers:
            response = requests.get("{}syncVoterDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentVoterDatabaseLength:
                largestVoterDatabase = jsonData["voters"]
                currentVoterDatabaseLength = jsonData["length"]

        # If there is no largestVoterDatabase then we sync current database with all nodes
        if largestVoterDatabase == None:
            largestVoterDatabase = voterDb.getAllVotersInJson()
            currentVoterDatabaseLength = voterDb.totalVoters()

        # If large voterDb is avialable sync it with current node
        if len(largestVoterDatabase) != voterDb.totalVoters():
            for voterData in largestVoterDatabase:
                newVoter = Voter.fromJson(voterData)
                voter = voterDb.getVoter(newVoter.voterId)

                # add if voter is None
                if voter == None:
                    voterDb.addVoter(newVoter)

        currentVoterDatabaseLength = voterDb.totalVoters()
        print("Syncing Voter Database with other nodes")

        # Sync largest voterDb among all nodes
        for node in peers:
            response = requests.get("{}syncVoterDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] != currentVoterDatabaseLength:
                resp = requests.post(
                    url="{}syncVoterDatabase".format(node),
                    json={"voters": voterDb.getAllVotersInJson()},
                    headers=POST_HEADERS,
                )
                if resp.status_code != 200:
                    print("Unable to Sync VoterDb with Node:", node)

        # Admin Database
        # -----------------------------------------------------------------------------

        print("Getting Admin Database")
        largestAdminDatabase = None
        currentAdminDatabaseLength = adminDb.totalAdmins()

        # Check if any long adminDb is avialable
        for node in peers:
            response = requests.get("{}syncAdminDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentAdminDatabaseLength:
                largestAdminDatabase = jsonData["admins"]
                currentAdminDatabaseLength = jsonData["length"]

        # If there is no largestVoterDatabase then we sync current database with all nodes
        if largestAdminDatabase == None:
            largestAdminDatabase = adminDb.getAllAdminsInJson()
            currentAdminDatabaseLength = adminDb.totalAdmins()

        # If long adminDb avialable sync it for current node
        if len(largestAdminDatabase) != adminDb.totalAdmins():
            for adminData in largestAdminDatabase:
                newAdmin = Admin.fromJson(adminData)
                admin = adminDb.getAdmin(newAdmin.loginId)

                # add if admin is None
                if admin == None:
                    adminDb.addAdmin(newAdmin)

        currentAdminDatabaseLength = adminDb.totalAdmins()
        print("Syncing Admin Database with other nodes")

        # Sync largest AdminDb among all nodes
        for node in peers:
            response = requests.get("{}syncAdminDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] != currentAdminDatabaseLength:
                resp = requests.post(
                    url="{}syncAdminDatabase".format(node),
                    json={"admins": adminDb.getAllAdminsInJson()},
                    headers=POST_HEADERS,
                )
                if resp.status_code != 200:
                    print("Unable to Sync AdminDb with Node:", node)

        return True
