from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

# from database import Voter


class VoterDatabase:
    """
    Class to manage admin database
    """

    def __init__(self) -> None:
        self.database = SQLAlchemy()
        # self.database.init_app(app)

    def initDatabase(self, app):
        """
        Command to create a fresh Database::
            run python or python3 in terminal
            >>> from database import voterDb
            >>> from ivote import iVoteApp
            >>> voterDb.initDatabase(app=iVoteApp)

        """
        self.database.create_all(app=app)

    def getAllVoters(self):
        from database import Voter

        return self.database.session.query(Voter).all()

    def getAllVotersInJson(self):
        from database import Voter

        votersInJson = []
        for voter in self.database.session.query(Voter).all():
            votersInJson.append(voter.toJson())

        return votersInJson

    def totalVoters(self):
        from database import Voter

        return self.database.session.query(Voter).count()

    def getVoter(self, voterId: str):
        from database import Voter

        return self.database.session.query(Voter).filter_by(voterId=voterId).first()

    def castVote(self, voterId: str):
        # from database import Voter

        try:
            voter = self.getVoter(voterId=voterId)

            if voter == None:
                return False, "Voter not found"

            voter.isVoteCasted = True
            self.database.session.commit()
            return True, "Voter casted and saved to database"
        # except IntegrityError:
        #     print("Voter Db Rollback\nUser already exists")
        #     self.database.session.rollback()
        #     return False
        except:
            print("Error: Updating Cast Vote in Db")
            return False, "Some error occured, Try again!"

    def changePassword(self, voterId: str, newPassowrd: str, name: str, district: str):
        # from database import Voter
        try:
            voter = self.getVoter(voterId=voterId)

            if voter == None:
                return False, "Voter not found"

            if voter.name != name or voter.district != district:
                return (
                    False,
                    "Verification Failed(Name & district doesnt match)\nPlease check your details",
                )

            voter.passwordHash = generate_password_hash(newPassowrd)
            self.database.session.commit()
            return True, "Password changed successfully"
        # except IntegrityError:
        #     print("Voter Db Rollback\nUser already exists")
        #     self.database.session.rollback()
        #     return False
        except:
            print("Error: Updating Password in VoterDb")
            return False, "Some error occured, Try again!"

    def addVoter(self, voter):
        try:
            self.database.session.add(voter)
            self.database.session.commit()
            return True, "Successfully registered"
        except IntegrityError:
            print("Voter Db Rollback\nUser already exists")
            self.database.session.rollback()
            return False, "Voter already exists! Please login"
        except:
            print("Error: Adding Voter in Db")
            return False, "Some error occured, Try again!"
