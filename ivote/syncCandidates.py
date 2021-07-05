from block.candidate import Candidate
from ivote import iVoteApp
from flask import request, jsonify
from blockchain import candidates, candidateList


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
                    "length": len(candidateList),
                    "candidates": candidates.getAllCandidatesInJson(),
                    "api": "/syncCandidates",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedCandidates = jsonData["candidates"]

                if len(candidateList) != len(receivedCandidates):
                    for candidateData in receivedCandidates:
                        candidate = Candidate.fromJson(candidateData)
                        if candidate.candidateId not in candidateList:
                            candidateList.append(candidate)

                    print("adding candidates done")
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncCandidates",
                                "message": "Successfully Added All Candidates",
                                "length": len(candidateList),
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
                                "length": len(candidateList),
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
