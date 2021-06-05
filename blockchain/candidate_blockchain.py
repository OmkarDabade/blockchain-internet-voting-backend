from block.candidate_block import CandidateBlock
import requests
from constants import genesisBlockHash, difficultyCandidateBlockchain, peers

# from blockchain import peers


class CandidateBlockchain:
    previousIndex = 0
    previousHash = None
    chain = []

    def addCandidateData(self, data):
        if len(self.chain) == 0:
            self.chain.append(
                CandidateBlock(
                    0,
                    data["candidateName"],
                    data["candidateId"],
                    data["state"],
                    data["district"],
                    data["ward"],
                    genesisBlockHash,
                )
            )
        else:
            self.chain.append(
                CandidateBlock(
                    self.previousIndex + 1,
                    data["candidateName"],
                    data["candidateId"],
                    data["state"],
                    data["district"],
                    data["ward"],
                    self.previousHash,
                )
            )
            self.previousIndex += 1
        self.previousHash = self.chain[-1].blockHash

    def acceptNewAnnouncedBlock(self, block):
        """
        A function that adds the newly announced block to the chain after verification.
        """

        if self.previousHash != block.previousHash:
            return False

        if not self.isValidProof(block, block.blockHash):
            return False

        self.chain.append(block)
        self.previousIndex += 1
        self.previousHash = block.blockHash

    @classmethod
    def isValidProof(cls, block, blockHash):
        """
        Check if blockHash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (
            blockHash.startswith("0" * difficultyCandidateBlockchain)
            and blockHash == block.computeHash()
        )

    @classmethod
    def checkChainValidity(cls, chain):
        result = True
        previousHash = genesisBlockHash

        for block in chain:

            if (
                not cls.isValidProof(block, block.blockHash)
                or previousHash != block.previousBlockHash
            ):
                result = False
                break

            previousHash = block.blockHash

        return result

    def announceNewBlock(block):
        """
        A function to announce to the network once a block has been mined.
        Other blocks can simply verify the proof of work and add it to their
        respective chains.
        """
        for peer in peers:
            url = "{}/add_block".format(peer)
            headers = {"Content-Type": "application/json"}
            requests.post(url=url, json=block.toJson(), headers=headers)
