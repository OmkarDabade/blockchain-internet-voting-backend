from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain

# API to search for proof of vote casted
@iVoteApp.route("/search", methods=["GET"])
def search():
    """
    Client-to-Node API
    """
    print("/search Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if "blockHash" in jsonData:
                for vote in blockchain.chain:
                    if vote.blockHash == jsonData["blockHash"]:
                        print(vote.blockHash)
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "message": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            elif "blockNo" in jsonData:
                for vote in blockchain.chain:
                    if vote.index == jsonData["blockNo"]:
                        print(vote.index)
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "message": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            elif "voterIdHash" in jsonData:
                for vote in blockchain.chain:
                    if vote.voterIdHash == jsonData["voterIdHash"]:
                        print(vote.voterIdHash)
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "message": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/search",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/search",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/search",
                "url": request.url,
            }
        )
