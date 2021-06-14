from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain


@iVoteApp.route("/search", methods=["GET"])
def search():
    print("/search Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if "blockHash" in jsonData:
                for vote in blockchain.chain:
                    print(vote.blockHash)
                    if vote.blockHash == jsonData["blockHash"]:
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "error": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            elif "blockNo" in jsonData:
                for vote in blockchain.chain:
                    print(vote.index)
                    if vote.index == jsonData["blockNo"]:
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "error": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            elif "fromVoter" in jsonData:
                for vote in blockchain.chain:
                    print(vote.fromVoter)
                    if vote.fromVoter == jsonData["fromVoter"]:
                        return vote.toJson()
                return jsonify(
                    {
                        "result": False,
                        "error": "Not Found",
                        "api": "/search",
                        "url": request.url,
                    }
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/search",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/search",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/search",
                "url": request.url,
            }
        )
