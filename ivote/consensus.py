from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain
from database import voterDb, adminDb, candidateDb
from constants import peers

# API to perform consensus
@iVoteApp.route("/consensus", methods=["POST"])
def consensus():
    """
    Test API
    Client-to-Node API
    """
    print("/consensus Called")
    print("DATA RECIEVED:", request.data)

    res = blockchain.consensus()

    if res:
        return jsonify(
            {
                "result": True,
                "message": "Consensus Performed",
                "api": "/consensus",
                "chain": len(blockchain.chain),
                "candidates": candidateDb.totalCandidates(),
                "peers": len(peers),
                "voters": voterDb.totalVoters(),
                "admins": adminDb.totalAdmins(),
                "url": request.url,
            }
        )
    else:
        return jsonify(
            {
                "result": False,
                "message": "Performing Consensus failed",
                "api": "/consensus",
                "url": request.url,
            }
        )
