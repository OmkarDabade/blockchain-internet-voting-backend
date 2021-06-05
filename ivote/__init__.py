from flask import Flask

# from flask_httpauth import HTTPBasicAuth

iVoteApp = Flask(__name__)
# auth = HTTPBasicAuth()

# from ivote.verify_password import verify_password

from .chain import chain, get_chain
from .index import index
from .cast_vote import cast_vote

from .login import login
from .search import search
from .add_candidate import add_candidate

from .get_candidates import get_candidates
from .add_block import add_block

from .create_chain_from_dump import create_chain_from_dump
from .register_from_new_node import register_from_new_node
