from flask.json import jsonify
from database import voterDb, adminDb
from flask import Flask
from flask_jwt_extended import JWTManager
from constants import ROLEADMIN, ROLEVOTER

# from flask_sqlalchemy import SQLAlchemy


iVoteApp = Flask(__name__)
# Setup the Flask-JWT-Extended extension
iVoteApp.config["JWT_SECRET_KEY"] = "This-Is-My-Super-Duper-Secret-Key-875"

# database name
iVoteApp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adminDatabase.db"
iVoteApp.config["SQLALCHEMY_BINDS"] = {
    ROLEADMIN: "sqlite:///adminDatabase.db",
    ROLEVOTER: "sqlite:///voterDatabase.db",
}
iVoteApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# creates SQLALCHEMY object
# voterDb = SQLAlchemy(app=iVoteApp)

voterDb.database.init_app(iVoteApp)
adminDb.database.init_app(iVoteApp)

# voterDb = SQLAlchemy()
# voterDb.init_app(iVoteApp)

jwt = JWTManager(iVoteApp)

from .addBlock import addBlock
from .addCandidate import addCandidate
from .addVoter import addVoter


from .castVote import castVote
from .chain import chain, get_chain
from .createChainFromDump import createChainFromDump

from .getCandidates import getCandidates
from .index import index
from .login import login

from .registerFromNewNode import registerFromNewNode
from .search import search
from .signup import signup


@iVoteApp.route("/voters", methods=["GET"])
def voters():
    print("/voters Called")
    chain = []
    for voter in voterDb.getAllVoters():
        chain.append(voter.toJson())

    return jsonify(
        {
            "Length": len(chain),
            "Voters": chain,
            "api": "/voters",
        }
    )


@iVoteApp.route("/admins", methods=["GET"])
def admins():
    print("/admins Called")
    chain = []
    for admin in adminDb.getAllAdmins():
        chain.append(admin.toJson())

    return jsonify(
        {
            "Length": len(chain),
            "Voters": chain,
            "api": "/admins",
        }
    )


# @jwt.additional_claims_loader
# def add_claims_to_access_token(identity):
#     print("IDENTITY:", identity)
#     return {
#         "role": ROLEADMIN,
#         "loginId": identity.loginId,
#         "name": identity.name,
#     }

# {
#     "aud": "some_audience",
#     "foo": "bar",
#     "upcase_name": identity.upper(),
# }
