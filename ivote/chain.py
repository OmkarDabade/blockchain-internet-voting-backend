from blockchain import voteBlockchain
from ivote import iVoteApp
from flask import jsonify


@iVoteApp.route("/chain")
def chain():
    chain = []
    for item in voteBlockchain.chain:
        chain.append(item.toJson())

    return jsonify({"votedChain": chain})
