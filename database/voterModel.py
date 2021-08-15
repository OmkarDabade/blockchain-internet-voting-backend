from constants import *
from database import voterDb
from sqlalchemy import Column, String, Boolean, Integer


# Database ORMs
class Voter(voterDb.database.Model):

    __tablename__ = "voters"
    __bind_key__ = ROLE_VOTER

    id = Column("Id", Integer, autoincrement=True, primary_key=True)
    voterId = Column("Voter Id", String(15), unique=True)
    name = Column("Name", String(60))
    state = Column("State", String(30))
    district = Column("District", String(40))
    ward = Column("Ward", Integer)
    isVoteCasted = Column("is Vote Casted", Boolean)
    mobile = Column("Mobile", Integer, unique=True)
    passwordHash = Column("Password Hash", String(150))

    def __init__(
        self,
        voterId: str,
        name: str,
        state: str,
        district: str,
        ward: int,
        mobile: int,
        passwordHash: str,
        isVoteCasted: bool = False,
    ) -> None:
        super().__init__()
        self.voterId = voterId
        self.name = name
        self.state = state
        self.district = district
        self.ward = ward
        self.mobile = mobile
        self.passwordHash = passwordHash
        self.isVoteCasted = isVoteCasted

    def toJson(self):
        return {
            "id": self.id,
            "voterId": self.voterId,
            "name": self.name,
            "state": self.state,
            "district": self.district,
            "ward": self.ward,
            "isVoteCasted": self.isVoteCasted,
            "mobile": self.mobile,
            "passwordHash": self.passwordHash,
        }

    @staticmethod
    def fromJson(jsonData: dict):
        return Voter(
            voterId=jsonData["voterId"],
            name=jsonData["name"],
            state=jsonData["state"],
            district=jsonData["district"],
            ward=jsonData["ward"],
            isVoteCasted=jsonData["isVoteCasted"],
            mobile=jsonData["mobile"],
            passwordHash=jsonData["passwordHash"],
        )
