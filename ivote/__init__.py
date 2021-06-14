from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


iVoteApp = Flask(__name__)
# Setup the Flask-JWT-Extended extension
iVoteApp.config["JWT_SECRET_KEY"] = "This-Is-My-Super-Duper-Secret-Key-875"

# database name
iVoteApp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voterDatabase.db"
iVoteApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# creates SQLALCHEMY object
# voterDb = SQLAlchemy(app=iVoteApp)
voterDb = SQLAlchemy()

voterDb.init_app(iVoteApp)

jwt = JWTManager(iVoteApp)


from .chain import chain, get_chain
from .index import index
from .castVote import castVote

from .login import login
from .search import search
from .addCandidate import addCandidate

from .getCandidates import getCandidates
from .addBlock import addBlock
from .signup import signup

from .createChainFromDump import createChainFromDump
from .registerFromNewNode import registerFromNewNode
