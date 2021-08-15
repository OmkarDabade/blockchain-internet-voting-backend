from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

# from werkzeug.security import generate_password_hash
# from database import Voter


class AdminDatabase:
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

    def getAllAdminsInJson(self):
        from database import Admin

        adminsInJson = []
        for admin in self.database.session.query(Admin).all():
            adminsInJson.append(admin.toJson())

        return adminsInJson

    def totalAdmins(self):
        from database import Admin

        return self.database.session.query(Admin).count()

    def getAdmin(self, loginId: str):
        from database import Admin

        admin = self.database.session.query(Admin).filter_by(loginId=loginId).first()
        print(admin)
        return admin

    def changePassword(self, loginId: str, newPassowrd: str, name: str):
        # from database import Voter
        try:
            admin = self.getAdmin(loginId=loginId)

            if admin == None:
                return False, "Admin not found"

            if admin.name != name:
                return (
                    False,
                    "Verification Failed(Name doesnt match)\nPlease check your details",
                )

            admin.passwordHash = generate_password_hash(newPassowrd)
            self.database.session.commit()
            return True, "Password changed successfully"
        # except IntegrityError:
        #     print("Voter Db Rollback\nUser already exists")
        #     self.database.session.rollback()
        #     return False
        except:
            print("Error: Updating Password in AdminDb")
            return False, "Some error occured, Try again!"

    def addAdmin(self, admin):
        try:
            self.database.session.add(admin)
            self.database.session.commit()
            return True, "Successfully registered"
        except IntegrityError:
            print("Admin Db Rollback\nUser already exists")
            self.database.session.rollback()
            return False, "Admin already exists! Please login"
        except:
            return False, "Some error occured, Try again!"
