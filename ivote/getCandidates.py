from ivote import iVoteApp
from flask import request, jsonify
from blockchain import candidateList


@iVoteApp.route("/getCandidates", methods=["GET"])
def getCandidates():
    """
    Client-to-Node API
    """

    print("/getCandidates Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()
            chain = []

            if len(jsonData) == 0:
                for candidate in candidateList:
                    print("Entered Loop")
                    chain.append(candidate.toJson())
                return (
                    jsonify(
                        {
                            "result": True,
                            "data": chain,
                            "api": "/getCandidates",
                            "url": request.url,
                        }
                    ),
                    200,
                )

            if "state" in jsonData and "district" in jsonData and "ward" in jsonData:
                print("Entered in 3")
                for candidate in candidateList:
                    print("Entered Loop")
                    if (
                        candidate.state == jsonData["state"]
                        and candidate.district == jsonData["district"]
                        and candidate.ward == jsonData["ward"]
                    ):
                        print("Match found")
                        chain.append(candidate.toJson())

                return (
                    jsonify(
                        {
                            "result": True,
                            "data": chain,
                            "api": "/getCandidates",
                            "url": request.url,
                        }
                    ),
                    200,
                )

            elif "state" in jsonData and "district" in jsonData:
                for candidate in candidateList:
                    if (
                        candidate.state == jsonData["state"]
                        and candidate.district == jsonData["district"]
                    ):
                        chain.append(candidate.toJson())

                return (
                    jsonify(
                        {
                            "result": True,
                            "data": chain,
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
                        "error": "Incomplete Data",
                        "api": "/getCandidates",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/getCandidates",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/getCandidates",
                "url": request.url,
            }
        )
