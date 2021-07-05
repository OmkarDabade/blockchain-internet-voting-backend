from database.voterModel import Voter
from ivote import iVoteApp
from flask import request, jsonify
from database import voterDb

# API to sync Voter database
@iVoteApp.route("/syncVoterDatabase", methods=["GET", "POST"])
def syncVoterDatabase():
    """
    Node-to-Node API
    """
    print("/syncVoterDatabase Called")

    try:
        if request.method == "GET":
            return jsonify(
                {
                    "result": True,
                    "length": voterDb.totalVoters(),
                    "voters": voterDb.getAllVotersInJson(),
                    "api": "/syncVoterDatabase",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedVoters = jsonData["voters"]

                if voterDb.totalVoters() != len(receivedVoters):
                    for voterData in receivedVoters:
                        newVoter = Voter.fromJson(voterData)
                        voter = voterDb.getVoter(newVoter.voterId)

                        if voter == None:
                            voterDb.addVoter(newVoter)

                    print("adding voters done")
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncVoterDatabase",
                                "message": "Successfully Synced VoterDb",
                                "length": voterDb.totalVoters(),
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncVoterDatabase",
                                "message": "VoterDb Already in Sync",
                                "length": voterDb.totalVoters(),
                                "url": request.url,
                            }
                        ),
                        200,
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Invalid JSON Format",
                        "api": "/syncVoterDatabase",
                        "url": request.url,
                    }
                )

    except AttributeError:
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/syncVoterDatabase",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncVoterDatabase",
                "url": request.url,
            }
        )
