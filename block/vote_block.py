from hashlib import sha256
from constants import *


class VoteBlock:
    index = 0
    voteFrom = None
    voteTo = None
    timestamp = None
    blockHash = None
    nonce = 0
    previousBlockHash = None

    def __init__(self, index, voteTo, voteFrom, timestamp, previousHash):
        self.index = index
        self.voteTo = voteTo
        self.voteFrom = voteFrom
        self.timestamp = timestamp
        self.previousBlockHash = previousHash
        self.computeProofOfWork()

    def computeHash(self):
        # blockString = json.dumps(self.__dict__, sort_keys=True)
        blockString = (
            str(self.index)
            + str(self.voteTo)
            + str(self.voteFrom)
            + str(self.timestamp)
            + str(self.nonce)
            + str(self.previousBlockHash)
        )
        return sha256(blockString.encode()).hexdigest()

    def computeProofOfWork(self):
        self.nonce = 0
        computedHash = self.computeHash()
        while not computedHash.startswith("0" * difficultyVoteBlockchain):
            self.nonce += 1
            computedHash = self.computeHash()
        self.blockHash = computedHash
        # return blockHash

    def __str__(self):
        return "\nBlock#: %s\nVote To: %s\nVote From: %s\nTime: %s\nNonce: %s\nHash: %s\nPrevious Hash: %s" % (
            self.index,
            self.voteTo,
            self.voteFrom,
            self.timestamp,
            self.nonce,
            self.blockHash,
            self.previousBlockHash,
        )

    def toJson(self):
        return {
            "Block#": self.index,
            "Vote To": self.voteTo,
            "Vote From": self.voteFrom,
            "Time": self.timestamp,
            "Nonce": self.nonce,
            "Hash": self.blockHash,
            "Previous Hash": self.previousBlockHash,
        }
