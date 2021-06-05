from ivote import iVoteApp
from flask import jsonify, request
from blockchain import voteBlockchain


@iVoteApp.route("/cast_vote", methods=["POST"])
# @auth.login_required
def cast_vote():
    print("/cast_vote Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            if "candidateId" in jsonData and "voterId" in jsonData:
                data = {
                    "voteTo": jsonData["candidateId"],
                    "timestamp": "JustNOW",
                    "voteFrom": jsonData["voterId"],
                }
                voteBlockchain.addBlock(data)
                return jsonify(
                    {
                        "result": True,
                        "data": voteBlockchain.chain[-1].toJson(),
                        "api": "/cast_vote",
                        "url": request.url,
                    }
                )
            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/cast_vote",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/cast_vote",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/cast_vote",
                "url": request.url,
            }
        )
