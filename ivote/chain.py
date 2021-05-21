from blockchain import voteBlockchain
from ivote import iVoteApp
from flask import jsonify


@iVoteApp.route("/chain", methods=["GET"])
def chain():
    chain = []
    for item in voteBlockchain.chain:
        chain.append(item.toJson())

    return jsonify({"total Blocks": len(chain), "vote BlockChain": chain})
