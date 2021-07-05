from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain, candidateList
from database import voterDb, adminDb
from constants import peers


@iVoteApp.route("/consensus", methods=["POST"])
def consensus():
    """
    Test API
    Client-to-Node API
    """
    print("/consensus Called")
    print("DATA RECIEVED:", request.data)

    blockchain.consensus()

    return jsonify(
        {
            "result": True,
            "message": "Consensus Performed",
            "api": "/consensus",
            "chain": len(blockchain.chain),
            "candidates": len(candidateList),
            "peers": len(peers),
            "voters": voterDb.totalVoters(),
            "admins": adminDb.totalAdmins(),
            "url": request.url,
        }
    )
