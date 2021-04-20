from hashlib import sha256
from constants import *


class CandidateBlock:
    index = 0
    candidateName = None
    candidateId = None
    candidateAgenda = None
    blockHash = None
    nonce = 0
    previousBlockHash = None

    def __init__(self, index, candidateName, candidateId, candidateAgenda, previousHash):
        self.index = index
        self.candidateName = candidateName
        self.candidateId = candidateId
        self.candidateAgenda = candidateAgenda
        self.previousBlockHash = previousHash
        self.computeProofOfWork()

    def computeHash(self):
        # blockString = json.dumps(self.__dict__, sort_keys=True)
        blockString = str(self.index) + str(self.candidateName) + str(
            self.candidateId) + str(self.candidateAgenda) + str(self.nonce) + str(self.previousBlockHash)
        return sha256(blockString.encode()).hexdigest()

    def computeProofOfWork(self):
        self.nonce = 0
        computedHash = self.computeHash()
        while not computedHash.startswith('0' * difficulty):
            self.nonce += 1
            computedHash = self.computeHash()
        self.blockHash = computedHash
        # return blockHash

    def __str__(self):
        return '\nBlock#: %s\nCandidate Id: %s\nCandidate Name: %s\nCandidate Agenda: %s\nNonce: %s\nHash: %s\nPrevious Hash: %s' % (self.index, self.candidateId, self.candidateName, self.candidateAgenda, self.nonce, self.blockHash, self.previousBlockHash)
