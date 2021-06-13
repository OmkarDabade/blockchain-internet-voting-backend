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
from .cast_vote import cast_vote

from .login import login
from .search import search
from .add_candidate import add_candidate

from .get_candidates import get_candidates
from .add_block import add_block
from .signup import signup

from .create_chain_from_dump import create_chain_from_dump
from .register_from_new_node import register_from_new_node
