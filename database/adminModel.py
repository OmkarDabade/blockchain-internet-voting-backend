from constants import *
from database import adminDb
from sqlalchemy import Column, String, Integer


# Database ORMs
class Admin(adminDb.database.Model):

    __tablename__ = "admins"
    __bind_key__ = ROLE_ADMIN

    id = Column("Id", Integer, autoincrement=True, primary_key=True)
    loginId = Column("Login Id", String(20), unique=True)
    name = Column("Name", String(60))
    passwordHash = Column("Password Hash", String(150))

    def __init__(self, name: str, loginId: str, passwordHash: str) -> None:
        super().__init__()
        self.name = name
        self.loginId = loginId
        self.passwordHash = passwordHash

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "loginId": self.loginId,
            "passwordHash": self.passwordHash,
        }

    @staticmethod
    def fromJson(jsonData: dict):
        return Admin(
            name=jsonData["name"],
            loginId=jsonData["loginId"],
            passwordHash=jsonData["passwordHash"],
        )
