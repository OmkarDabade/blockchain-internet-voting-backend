from blockchain import voteBlockchain
from ivote import iVoteApp
from flask import jsonify


@iVoteApp.route("/chain")
def getChain():
    chain = []
    for item in voteBlockchain.blockchain:
        chain.append(item.toJson())

    return jsonify({"votedChain": chain})
