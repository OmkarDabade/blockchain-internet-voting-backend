from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

# from database import Voter


class AdminDatabase:
    def __init__(self) -> None:
        self.database = SQLAlchemy()
        # self.database.init_app(app)

    def initDatabase(self, app):
        """
        Command to create a fresh Database::
            run python or python3 in terminal
            >>> from database import adminDb
            >>> from ivote import iVoteApp
            >>> adminDb.initDatabase(app=iVoteApp)

        """
        # from database import Admin

        self.database.create_all(app=app)
        # self.database.session.add(
        #     Admin(
        #         name="Admin",
        #         loginId="admin",
        #         passwordHash=generate_password_hash("admin"),
        #     )
        # )
        # self.database.session.commit()

    def getAllAdmins(self):
        from database import Admin

        return self.database.session.query(Admin).all()

    def getAdmin(self, loginId: str):
        from database import Admin

        admin = self.database.session.query(Admin).filter_by(loginId=loginId).first()
        print(admin)
        return admin

    def addAdmin(self, admin):
        try:
            self.database.session.add(admin)
            self.database.session.commit()
            return True
        except IntegrityError:
            print("Admin Db Rollback\nUser already exists")
            self.database.session.rollback()
            return False
        except:
            return False
