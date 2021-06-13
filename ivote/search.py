from ivote import iVoteApp
from flask import request, jsonify
from blockchain import voteBlockchain


@iVoteApp.route("/search", methods=["GET"])
def search():
    print("/search Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            if "blockHash" in jsonData:
                for item in voteBlockchain.chain:
                    print(item.blockHash)
                    if item.blockHash == jsonData["blockHash"]:
                        return item.toJson()

            elif "blockNo" in jsonData:
                for item in voteBlockchain.chain:
                    print(item.index)
                    if item.index == jsonData["blockNo"]:
                        return item.toJson()

            elif "voteFrom" in jsonData:
                for item in voteBlockchain.chain:
                    print(item.voteFrom)
                    if item.voteFrom == jsonData["voteFrom"]:
                        return item.toJson()

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