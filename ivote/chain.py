from blockchain import blockchain
from ivote import iVoteApp
from flask import jsonify, request
from constants import peers

# API to get chain data
@iVoteApp.route("/chain", methods=["GET"])
def chain():
    """
    Client-to-Node API\n
    Authority-to-Node API
    """
    print("/chain Called")

    return jsonify(
        {
            "result": True,
            "length": len(blockchain.chain),
            "chain": blockchain.getChainInJson(),
            "peers": len(peers),
            "url": request.url,
            "api": "/chain",
        }
    )
