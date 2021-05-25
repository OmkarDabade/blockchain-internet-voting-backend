from flask import Flask

# from flask_httpauth import HTTPBasicAuth


iVoteApp = Flask(__name__)
# auth = HTTPBasicAuth()

# from ivote.verify_password import verify_password

from ivote.chain import chain
from ivote.index import index
from ivote.cast_vote import cast_vote
from ivote.login import login
from ivote.search import search
from ivote.add_candidate import add_candidate
from ivote.get_candidates import get_candidates
