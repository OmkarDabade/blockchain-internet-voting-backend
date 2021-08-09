from blockchain import blockchain
from database import adminRequired
from ivote import iVoteApp
from flask import request, jsonify
from database import candidateDb

# API to add new candidate to current node
@iVoteApp.route("/addCandidate", methods=["POST"])
@adminRequired(api="/addCandidate")
def addCandidate():
    """
    Node-to-Node API\n
    Auhority-to-Node API
    """
    print("/addCandidate Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if (
                "candidateId" in jsonData
                and "candidateName" in jsonData
                and "state" in jsonData
                and "district" in jsonData
                and "ward" in jsonData
            ):
                added, msg = candidateDb.addCandidate(
                    jsonData["candidateId"],
                    jsonData["candidateName"],
                    jsonData["state"],
                    jsonData["district"],
                    jsonData["ward"],
                )

                if added:
                    print("Candidate Added")
                    blockchain.consensus()
                else:
                    print("Error Adding Candidate")
                    print(msg)

                return jsonify(
                    {
                        "result": added,
                        # "data": candidateDb.candidatesList[-1].toJson(),
                        "message": msg,
                        "api": "/addCandidate",
                        "url": request.url,
                    }
                )
            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/addCandidate",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/addCandidate",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/addCandidate",
                "url": request.url,
            }
        )
