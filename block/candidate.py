from constants import *


class Candidate:
    """
    To Store Candidate Data
    """

    def __init__(
        self,
        index: int,
        candidateId: int,
        candidateName: str,
        state: str,
        district: str,
        ward: int,
    ):
        self.index = index
        self.candidateName = candidateName
        self.candidateId = candidateId
        self.state = state
        self.district = district
        self.ward = ward

    def __str__(self):
        return "\nBlock#: %s\nCandidate Id: %s\nCandidate Name: %s\nState: %s\nDistrict: %s\nWard#: %s" % (
            self.index,
            self.candidateId,
            self.candidateName,
            self.state,
            self.district,
            self.ward,
        )

    def toJson(self):
        return {
            "block#": self.index,
            "candidateId": self.candidateId,
            "candidateName": self.candidateName,
            "state": self.state,
            "district": self.district,
            "ward": self.ward,
        }
