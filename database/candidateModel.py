from database import candidateDb
from constants import *
from sqlalchemy import Column, String, Integer


# Database ORMs
class Candidate(candidateDb.database.Model):

    __tablename__ = "candidates"
    __bind_key__ = CANDIDATES

    candidateId = Column("Id", Integer, autoincrement=True, primary_key=True)
    candidateName = Column("Name", String(60))
    state = Column("State", String(50))
    district = Column("District", String(50))
    ward = Column("Ward", Integer)

    def __init__(
        self,
        candidateId: int,
        candidateName: str,
        state: str,
        district: str,
        ward: int,
    ):
        super().__init__()
        self.candidateId = candidateId
        self.candidateName = candidateName
        self.state = state
        self.district = district
        self.ward = ward

    def toJson(self):
        return {
            "candidateId": self.candidateId,
            "candidateName": self.candidateName,
            "state": self.state,
            "district": self.district,
            "ward": self.ward,
        }

    @staticmethod
    def fromJson(jsonData: dict):
        return Candidate(
            jsonData["candidateId"],
            jsonData["candidateName"],
            jsonData["state"],
            jsonData["district"],
            jsonData["ward"],
        )

    def __str__(self):
        return (
            "\nCandidate Id: %s\nCandidate Name: %s\nState: %s\nDistrict: %s\nWard#: %s"
            % (
                self.candidateId,
                self.candidateName,
                self.state,
                self.district,
                self.ward,
            )
        )
