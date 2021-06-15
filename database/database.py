from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# from database import Voter


class VoterDatabase:
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

    def getVoter(self, voterId: str):
        from database import Voter

        return self.database.session.query(Voter).filter_by(voterId=voterId).first()

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
            return False
