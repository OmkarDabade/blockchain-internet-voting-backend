from ivote import iVoteApp
from flask import request, jsonify
import requests
from constants import peers, POST_HEADERS
from blockchain import blockchain

# API to register new node of network and perform a sync operation
@iVoteApp.route("/registerFromNewNode", methods=["POST"])
def registerFromNewNode():
    """
    Node-to-Node API
    """
    print("/registerFromNewNode Called")
    print("DATA RECIEVED:", request.data)

    if request.is_json:
        jsonData = request.get_json()
        newNodeAddress = jsonData["newNodeAddress"]

        if newNodeAddress == None:
            return jsonify(
                {
                    "result": False,
                    "message": "Node Address not avialable in request",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )
        # Add the node to the peer list
        peers.add(str(newNodeAddress))

        res = blockchain.consensus()

        if res:
            return jsonify(
                {
                    "result": True,
                    "message": "Registration Successful and Data Synced",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )
        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Data Sync Failed",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )

    else:
        return jsonify(
            {
                "result": False,
                "message": "Invalid JSON Format",
                "api": "/registerFromNewNode",
                "url": request.url,
            }
        )
