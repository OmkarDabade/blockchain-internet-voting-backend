from flask import Flask

iVoteApp = Flask(__name__)

from ivote.chain import getChain
from ivote.index import index
