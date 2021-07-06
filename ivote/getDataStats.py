from ivote import iVoteApp
from flask import request, jsonify
from constants import peers
from blockchain import blockchain, candidateList
from database import voterDb, adminDb

# API to get stats of all data
@iVoteApp.route("/getDataStats", methods=["GET"])
def getDataStats():
    """
    Authority-to-Node API
    """
    print("/getDataStats Called")
    print("DATA RECIEVED:", request.data)

    return jsonify(
        {
            "result": True,
            "api": "/getDataStats",
            "url": request.url,
            "chain": len(blockchain.chain),
            "candidates": len(candidateList),
            "peers": len(peers),
            "voters": voterDb.totalVoters(),
            "admins": adminDb.totalAdmins(),
        }
    )
