from datetime import datetime
from constants import *
from hashlib import sha256


class Vote:
    def __init__(
        self,
        index: int,
        candidateId: int,
        candidateName: str,
        fromVoter: str,
        timestamp: datetime,
        previousHash: str,
        blockHash: str = None,
        nonce: int = 0,
    ):
        self.index = index
        self.candidateId = candidateId
        self.candidateName = candidateName
        self.fromVoter = fromVoter
        self.timestamp = timestamp
        self.previousBlockHash = previousHash
        if blockHash is not None:
            self.blockHash = blockHash
            self.nonce = nonce
        else:
            self.computeProofOfWork()

    def computeHash(self):
        # blockString = json.dumps(self.__dict__, sort_keys=True)
        blockString = (
            str(self.index)
            + str(self.candidateId)
            + str(self.candidateName)
            + str(self.fromVoter)
            + str(self.timestamp)
            + str(self.nonce)
            + str(self.previousBlockHash)
        )
        return sha256(blockString.encode()).hexdigest()

    def computeProofOfWork(self):
        self.nonce = 0
        computedHash = self.computeHash()
        while not computedHash.startswith("0" * blockchainDifficulty):
            self.nonce += 1
            computedHash = self.computeHash()
        self.blockHash = computedHash
        # return blockHash

    def __str__(self):
        return "\nBlock#: %s\nCandidate Id: %s\nCandidate Name: %s\nFrom Voter: %s\nTime: %s\nNonce: %s\nBlock Hash: %s\nPrevious Hash: %s" % (
            self.index,
            self.candidateId,
            self.candidateName,
            self.fromVoter,
            self.timestamp,
            self.nonce,
            self.blockHash,
            self.previousBlockHash,
        )

    def toJson(self):
        return {
            "block#": self.index,
            "candidateId": self.candidateId,
            "candidateName": self.candidateName,
            "fromVoter": self.fromVoter,
            "time": self.timestamp,
            "nonce": self.nonce,
            "blockHash": self.blockHash,
            "previousHash": self.previousBlockHash,
        }
