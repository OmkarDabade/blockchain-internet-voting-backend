from ivote import iVoteApp
from flask import jsonify, request
from blockchain import blockchain
from flask_jwt_extended import jwt_required


@iVoteApp.route("/castVote", methods=["POST"])
@jwt_required()
def castVote():
    """
    Client-to-Node API
    """

    print("/castVote Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if (
                "candidateId" in jsonData
                and "candidateName" in jsonData
                and "fromVoter" in jsonData
            ):
                blockchain.addBlock(
                    jsonData["candidateId"],
                    jsonData["candidateName"],
                    jsonData["fromVoter"],
                )
                return jsonify(
                    {
                        "result": True,
                        "data": blockchain.chain[-1].toJson(),
                        "api": "/castVote",
                        "url": request.url,
                    }
                )
            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/castVote",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/castVote",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/castVote",
                "url": request.url,
            }
        )
