from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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
                return False

            voter.isVoteCasted = True
            self.database.session.commit()
            return True
        except IntegrityError:
            print("Voter Db Rollback\nUser already exists")
            self.database.session.rollback()
            return False
        except:
            print("Error: Updating Cast Vote in Db")
            return False

    def addVoter(self, voter):
        try:
            self.database.session.add(voter)
            self.database.session.commit()
            return True
        except IntegrityError:
            print("Voter Db Rollback\nUser already exists")
            self.database.session.rollback()
            return False
        except:
            print("Error: Adding Voter in Db")
            return False
