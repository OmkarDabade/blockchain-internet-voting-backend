from flask_jwt_extended.view_decorators import jwt_required
from ivote import iVoteApp
from flask import request, jsonify
from database import candidateDb

# API to get list of candidates to whom vote will be casted
@iVoteApp.route("/getCandidates", methods=["POST"])
@jwt_required()
def getCandidates():
    """
    Client-to-Node API
    """
    print("/getCandidates Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()
            candidatesListToSend = []

            if len(jsonData) == 0:
                for candidate in candidateDb.allCandidates():
                    candidatesListToSend.append(candidate.toJson())
                print("Sending all candidates")
                return (
                    jsonify(
                        {
                            "result": True,
                            "candidates": candidatesListToSend,
                            "api": "/getCandidates",
                            "url": request.url,
                        }
                    ),
                    200,
                )
            elif "state" in jsonData and "district" in jsonData and "ward" in jsonData:
                print("Sending all candidates state, district and ward wise")
                for candidate in candidateDb.allCandidates():
                    print("Entered Loop")
                    if (
                        candidate.state == jsonData["state"]
                        and candidate.district == jsonData["district"]
                        and candidate.ward == jsonData["ward"]
                    ):
                        candidatesListToSend.append(candidate.toJson())
                        print("Match found")
                return (
                    jsonify(
                        {
                            "result": True,
                            "candidates": candidatesListToSend,
                            "api": "/getCandidates",
                            "url": request.url,
                        }
                    ),
                    200,
                )

            elif "state" in jsonData and "district" in jsonData:
                print("Sending all candidates state and district wise")
                for candidate in candidateDb.allCandidates():
                    if (
                        candidate.state == jsonData["state"]
                        and candidate.district == jsonData["district"]
                    ):
                        candidatesListToSend.append(candidate.toJson())
                        print("Match found")
                return (
                    jsonify(
                        {
                            "result": True,
                            "candidates": candidatesListToSend,
                            "api": "/getCandidates",
                            "url": request.url,
                        }
                    ),
                    200,
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/getCandidates",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/getCandidates",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/getCandidates",
                "url": request.url,
            }
        )
