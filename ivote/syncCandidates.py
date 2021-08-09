from database.candidateModel import Candidate
from ivote import iVoteApp
from flask import request, jsonify
from database import candidateDb

# API to sync list of candidates
@iVoteApp.route("/syncCandidates", methods=["GET", "POST"])
def syncCandidates():
    """
    Node-to-Node API
    """
    print("/syncCandidates Called")

    try:
        if request.method == "GET":
            return jsonify(
                {
                    "result": True,
                    "length": candidateDb.totalCandidates(),
                    "candidates": candidateDb.getAllCandidatesInJson(),
                    "api": "/syncCandidates",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedCandidates = jsonData["candidates"]
                added, msg = None

                if candidateDb.totalCandidates() != len(receivedCandidates):
                    for candidateData in receivedCandidates:
                        candidate = Candidate.fromJson(candidateData)
                        if candidate.candidateId not in candidateDb.allCandidates():
                            added, msg = candidateDb.addCandidate(
                                candidate.candidateId,
                                candidate.candidateName,
                                candidate.state,
                                candidate.district,
                                candidate.ward,
                            )

                    print("adding candidates done")
                    return (
                        jsonify(
                            {
                                "result": added,
                                "api": "/syncCandidates",
                                "message": msg,
                                "length": candidateDb.totalCandidates(),
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
                                "api": "/syncCandidates",
                                "message": "Candidates Already in Sync",
                                "length": candidateDb.totalCandidates(),
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
                        "api": "/syncCandidates",
                        "url": request.url,
                    }
                )

    except AttributeError:
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/syncCandidates",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncCandidates",
                "url": request.url,
            }
        )
