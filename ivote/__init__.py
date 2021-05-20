from flask import Flask

iVoteApp = Flask(__name__)

from ivote.chain import chain
from ivote.index import index
from ivote.cast_vote import castVote
from ivote.login import login
from ivote.search import search
