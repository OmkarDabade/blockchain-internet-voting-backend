from database.voterModel import Voter
from database.adminModel import Admin
from flask.json import jsonify
from database import voterDb, adminDb
from flask import Flask
from flask_jwt_extended import JWTManager
from constants import ROLE_ADMIN, ROLE_VOTER

iVoteApp = Flask(__name__)
# Setup the Flask-JWT-Extended extension
iVoteApp.config["JWT_SECRET_KEY"] = "This-Is-My-Super-Duper-Secret-Key-875"

# database name
iVoteApp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adminDatabase.db"
iVoteApp.config["SQLALCHEMY_BINDS"] = {
    ROLE_ADMIN: "sqlite:///adminDatabase.db",
    ROLE_VOTER: "sqlite:///voterDatabase.db",
}
iVoteApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

voterDb.database.init_app(iVoteApp)
adminDb.database.init_app(iVoteApp)

jwt = JWTManager(iVoteApp)

from .addBlock import addBlock
from .addCandidate import addCandidate
from .addVoter import addVoter

from .castVote import castVote
from .chain import chain
from .consensus import consensus

from .getCandidates import getCandidates
from .getDataStats import getDataStats

from .index import index
from .login import login

from .registerFromNewNode import registerFromNewNode
from .search import search
from .signup import signup

from .syncAdminDatabase import syncAdminDatabase
from .syncCandidates import syncCandidates

from .syncChain import syncChain
from .syncPeers import syncPeers
from .syncVoterDatabase import syncVoterDatabase


@iVoteApp.route("/voters", methods=["GET"])
def voters():
    print("/voters Called")
    print("QUERY: ", str(voterDb.database.session.query(Voter).count()))
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
    print("QUERY: ", str(adminDb.database.session.query(Admin).count()))

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
