from constants import *
from hashlib import sha256


class CandidateBlock:
    def __init__(
        self,
        index,
        candidateId,
        candidateName,
        state,
        district,
        ward,
        previousBlockHash,
        nonce=0,
        blockHash=None,
    ):
        self.index = index
        self.candidateName = candidateName
        self.candidateId = candidateId
        self.state = state
        self.district = district
        self.ward = ward
        self.previousBlockHash = previousBlockHash
        if blockHash is not None:
            self.blockHash = blockHash
            self.nonce = nonce
        else:
            self.computeProofOfWork()

    def computeHash(self):
        # blockString = json.dumps(self.__dict__, sort_keys=True)
        blockString = (
            str(self.index)
            + str(self.candidateName)
            + str(self.candidateId)
            + str(self.state)
            + str(self.district)
            + str(self.ward)
            + str(self.nonce)
            + str(self.previousBlockHash)
        )
        return sha256(blockString.encode()).hexdigest()

    def computeProofOfWork(self):
        self.nonce = 0
        computedHash = self.computeHash()

        while not computedHash.startswith("0" * difficultyCandidateBlockchain):
            self.nonce += 1
            computedHash = self.computeHash()
        self.blockHash = computedHash
        # return blockHash

    def __str__(self):
        return "\nBlock#: %s\nCandidate Id: %s\nCandidate Name: %s\nState: %s\nDistrict: %s\nWard#: %s\nNonce: %s\nBlock Hash: %s\nPrevious Hash: %s" % (
            self.index,
            self.candidateId,
            self.candidateName,
            self.state,
            self.district,
            self.ward,
            self.nonce,
            self.blockHash,
            self.previousBlockHash,
        )

    def toJson(self):
        return {
            "Block#": self.index,
            "Candidate Id": self.candidateId,
            "Candidate Name": self.candidateName,
            "State": self.state,
            "District": self.district,
            "Ward#": self.ward,
            "Nonce": self.nonce,
            "Block Hash": self.blockHash,
            "Previous Hash": self.previousBlockHash,
        }
