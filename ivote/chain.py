from flask.globals import request
from blockchain import voteBlockchain
from ivote import iVoteApp
from flask import jsonify
from constants import peers

# endpoint to return the node's copy of the chain.
@iVoteApp.route("/chain", methods=["GET"])
def chain():
    print("/chain Called")
    chain = []
    for block in voteBlockchain.chain:
        chain.append(block.toJson())

    return jsonify(
        {
            "Length": len(chain),
            "Chain": chain,
            "Peers": list(peers),
            "url": request.url,
            "api": "/chain",
        }
    )


def get_chain():
    print("/get_chain Called")
    chain = []
    for block in voteBlockchain.chain:
        chain.append(block.toJson())

    return {
        "Length": len(chain),
        "Chain": chain,
        "Peers": list(peers),
        "url": request.url,
        "api": "/chain",
    }
