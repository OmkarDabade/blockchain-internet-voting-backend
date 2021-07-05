from hashlib import sha1
from ivote import iVoteApp
from flask import jsonify, request
from blockchain import blockchain
from flask_jwt_extended import jwt_required
from database import voterDb


@iVoteApp.route("/castVote", methods=["POST"])
# @jwt_required()
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
                and "voterId" in jsonData
            ):
                voter = voterDb.getVoter(jsonData["voterId"])

                if voter == None:
                    return jsonify(
                        {
                            "result": False,
                            "message": "Voter not found",
                            "api": "/castVote",
                            "url": request.url,
                        }
                    )

                if voter.isVoteCasted:
                    return jsonify(
                        {
                            "result": True,
                            "message": "Vote Already Casted",
                            "voterId": sha1(jsonData["voterId"].encode()).hexdigest(),
                            "api": "/castVote",
                            "url": request.url,
                        }
                    )

                blockchain.addBlock(
                    jsonData["candidateId"],  # CandidateId
                    jsonData["candidateName"],  # CandidateName
                    jsonData["voterId"],  # VoterId
                )

                voteCasted = voterDb.castVote(jsonData["voterId"])

                vote = blockchain.chain[-1]
                # vote.voterId = sha1(vote.voterId.encode()).hexdigest()

                return jsonify(
                    {
                        "result": True,
                        "data": vote.toJson(),
                        "api": "/castVote",
                        "url": request.url,
                    }
                )
            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/castVote",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/castVote",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/castVote",
                "url": request.url,
            }
        )
