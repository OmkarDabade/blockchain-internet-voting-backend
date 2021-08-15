from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


class CandidateDatabase:
    """
    Class to manage candidate database
    """

    def __init__(self) -> None:
        self.database = SQLAlchemy()
        # self.database.init_app(app)

    def initDatabase(self, app):
        """
        Command to create a fresh Database::
            run python or python3 in terminal
            >>> from database import candidateDb
            >>> from ivote import iVoteApp
            >>> candidateDb.initDatabase(app=iVoteApp)

        """
        # from database import Admin

        self.database.create_all(app=app)
        # self.database.session.add(
        #     Candidate(
        #     )
        # )
        # self.database.session.commit()

    def allCandidates(self):
        from database import Candidate

        return self.database.session.query(Candidate).all()

    def getAllCandidatesInJson(self):
        from database import Candidate

        candidatesInJson: list[dict] = []
        for candidate in self.database.session.query(Candidate).all():
            candidatesInJson.append(candidate.toJson())

        return candidatesInJson

    def totalCandidates(self):
        from database import Candidate

        return self.database.session.query(Candidate).count()

    def addCandidate(
        self, candidateId: int, candidateName: str, state: str, district: str, ward: int
    ):
        """
        Function to add candidate in list
        """
        from database import Candidate

        try:
            self.database.session.add(
                Candidate(candidateId, candidateName, state, district, ward)
            )
            self.database.session.commit()
            return True, "Successfully Added"
        except IntegrityError:
            print("Candidate Db Rollback\Candidate already exists")
            self.database.session.rollback()
            return False, "Candidate with current Id already exists!"
        except:
            return False, "Some error occured, Try again!"

    """
    Class to store list of candidates
    """

    # candidatesList: list[Candidate] = []

    # def announceNewCandidate(self, candidate: Candidate):
    #     """
    #     A function to announce to the network a new candidate.
    #     """
    #     print("Annoucing New Candidate To Peers")

    #     if len(peers) == 0:
    #         print("no registered peers, returning...")
    #         return

    #     for peer in peers:
    #         url = "{}addCandidate".format(peer)
    #         res = requests.post(url=url, json=candidate.toJson(), headers=POST_HEADERS)

    #         print("Peer: ", peer)
    #         print("API Response: ", res.text)
