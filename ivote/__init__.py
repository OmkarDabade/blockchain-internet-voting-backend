from database.voterModel import Voter
from database.adminModel import Admin
from flask.json import jsonify
from database import voterDb, adminDb, candidateDb
from flask import Flask
from flask_jwt_extended import JWTManager
from constants import CANDIDATES, ROLE_ADMIN, ROLE_VOTER
from flask_cors import CORS

iVoteApp = Flask(__name__)

# To use this flask api app on other platforms other than curl
# Cross Origin Resource Sharing (CORS)
CORS(iVoteApp)

# Setup the Flask-JWT-Extended extension
iVoteApp.config["JWT_SECRET_KEY"] = "This-Is-My-Super-Duper-Secret-Key-875"

# database name
iVoteApp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adminDatabase.db"
iVoteApp.config["SQLALCHEMY_BINDS"] = {
    ROLE_ADMIN: "sqlite:///adminDatabase.db",
    ROLE_VOTER: "sqlite:///voterDatabase.db",
    CANDIDATES: "sqlite:///candidateDatabase.db",
}
iVoteApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

voterDb.database.init_app(iVoteApp)
adminDb.database.init_app(iVoteApp)
candidateDb.database.init_app(iVoteApp)

jwt = JWTManager(iVoteApp)

from .addBlock import addBlock
from .addCandidate import addCandidate
from .addVoter import addVoter

from .castVote import castVote
from .chain import chain
from .consensus import consensus

from .forgotPassword import forgotPassword
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
