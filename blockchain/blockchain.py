from hashlib import sha1
from database.adminModel import Admin
from database.voterModel import Voter
from block.candidate import Candidate
from . import candidateList, candidates
from block.vote import Vote
from constants import *
import requests
from datetime import datetime
from flask import request
from database import voterDb, adminDb


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
        A function that adds the block to the chain.
        """
        print("Adding Block to chain")

        if len(self.chain) == 0:
            newBlock = Vote(
                0,
                candidateId,
                candidateName,
                # voterId,
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
                # voterId,
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

        # if len(self.chain) == 0:
        print("Previous     HASH:", self.previousHash)
        print("Recived BlockHASH:", block.previousBlockHash)

        if self.previousHash != block.previousBlockHash:
            print("Hash doesnt match")
            return False

        if not self.isValidProof(block, block.blockHash):
            print("is not valid proof")
            return False

        # else:
        #     print("Previous     HASH:", self.previousHash)
        #     print("Recived BlockHASH:", block.previousBlockHash)

        #     if self.previousHash != block.previousBlockHash:
        #         print("Hash doesnt match")
        #         return False

        #     if not self.isValidProof(block, block.blockHash):
        #         print("is not valid proof")
        #         return False

        print("Block added to chain")
        self.chain.append(block)
        self.previousIndex += 1
        self.previousHash = block.blockHash
        return True

    @classmethod
    def isValidProof(cls, block: Vote, blockHash: str):
        """
        Check if blockHash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (
            blockHash.startswith("0" * BLOCKCHAIN_DIFFICULTY)
            and blockHash == block.computeHash()
        )

    @classmethod
    def isChainValid(cls, chainDump: dict):
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
        res = self.isChainValid(chainDump)
        if res:
            newChain: list[Vote] = []

            for voteData in chainDump:
                vote = Vote.fromJson(voteData)
                newChain.append(vote)

            self.chain = newChain
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
            # headers = {"Content-Type": "application/json"}
            print(url)
            # try:
            res = requests.post(url=url, json=block.toJson(), headers=POST_HEADERS)
            print("Peer: ", peer)
            print("API Response ", res.text)
            if res.status_code == 200:
                jsonData = res.json()
                print("Result: ", jsonData["result"])

                # if jsonData["result"] == True:
                #     print("res is True")
                #     if jsonData["data"]["Length"] != len(self.chain):
                #         self.consensus()
            # except:
            #     print("Some error occured during annoucing block")

    def getChainInJson(self):
        chain = []
        for vote in self.chain:
            # vote.voterId = sha1(vote.voterId.encode()).hexdigest()
            chain.append(vote.toJson())

        return chain

    def consensus(self):
        """
        Our naive consensus algorithm. If a longer valid chain is
        found, our chain is replaced with it.
        """
        print("Consensous called")

        if len(peers) == 0:
            print("No registerd peers, returning...")
            return

        print("URL:", request.url)
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

        # If long peer list avialable sync it with current node
        if longestPeerList:
            for peer in longestPeerList:
                if request.host_url != peer:
                    peers.add(str(peer))

            newPeers: list = list(peers)
            newPeers.append(request.host_url)

            # longestPeerList = None
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

        # If longest valid chain avialable sync it with current node
        if longestValidChainDump:
            self.syncChain(longestValidChainDump)

            # longestPeerList = None
            currentChainLength = len(self.chain)
            print("Syncing chain with current node")

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

        print("Syncing Candidates")
        longestCandidateData = None
        currentCandidateDataLength = len(candidateList)

        # Check for longest candidate list
        for node in peers:
            response = requests.get("{}syncCandidates".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentCandidateDataLength:
                longestCandidateData = jsonData["candidates"]
                currentCandidateDataLength = jsonData["length"]

        # If longest candidate list avialable sync it with current node
        if longestCandidateData:
            for candidateData in longestCandidateData:
                candidate = Candidate.fromJson(candidateData)
                if candidate.candidateId not in candidateList:
                    candidateList.append(candidate)

            currentCandidateDataLength = len(candidateList)
            print("Syncing Candidates")

            # Sync longest candidate list among all nodes
            for node in peers:
                response = requests.get("{}syncCandidates".format(node))
                jsonData = response.json()
                if jsonData["length"] != currentCandidateDataLength:
                    resp = requests.post(
                        url="{}syncCandidates".format(node),
                        json={"candidates": candidates.getAllCandidatesInJson()},
                        headers=POST_HEADERS,
                    )
                    if resp.status_code != 200:
                        print("Unable to Sync Canidates with Node:", node)

        # Voter Database
        # -----------------------------------------------------------------------------

        print("Syncing Voter Database")
        largestVoterDatabase = None
        currentVoterDatabaseLength = voterDb.totalVoters()

        # Check if largest voterDb is avialable
        for node in peers:
            response = requests.get("{}syncVoterDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentVoterDatabaseLength:
                largestVoterDatabase = jsonData["voters"]
                currentVoterDatabaseLength = jsonData["length"]

        # If large voterDb is avialable sync it with current node
        if largestVoterDatabase:
            for voterData in largestVoterDatabase:
                newVoter = Voter.fromJson(voterData)
                voter = voterDb.getVoter(newVoter.voterId)

                # add if voter is None
                if voter == None:
                    voterDb.addVoter(newVoter)

            currentVoterDatabaseLength = voterDb.totalVoters()
            print("Syncing VoterDb")

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

        print("Syncing Admin Database")
        largestAdminDatabase = None
        currentAdminDatabaseLength = adminDb.totalAdmins()

        # Check if any long adminDb is avialable
        for node in peers:
            response = requests.get("{}syncAdminDatabase".format(node))
            jsonData = response.json()
            if jsonData["length"] > currentAdminDatabaseLength:
                largestAdminDatabase = jsonData["admins"]
                currentAdminDatabaseLength = jsonData["length"]

        # If long adminDb avialable sync it for current node
        if largestAdminDatabase:
            for adminData in largestAdminDatabase:
                newAdmin = Admin.fromJson(adminData)
                admin = adminDb.getAdmin(newAdmin.loginId)

                # add if admin is None
                if admin == None:
                    adminDb.addAdmin(newAdmin)

            currentAdminDatabaseLength = adminDb.totalAdmins()
            print("Syncing AdminDb")

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
