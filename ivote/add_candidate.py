from ivote import iVoteApp
from flask import request, jsonify
from blockchain import candidateBlockchain


@iVoteApp.route("/add_candidate", methods=["POST"])
def add_candidate():
    try:
        if request.is_json:
            jsonData = request.get_json()
            print(jsonData)

            if (
                "candidateId" in jsonData
                and "candidateName" in jsonData
                and "state" in jsonData
                and "district" in jsonData
                and "ward" in jsonData
            ):
                data = {
                    "candidateName": jsonData["candidateName"],
                    "candidateId": jsonData["candidateId"],
                    "state": jsonData["state"],
                    "district": jsonData["district"],
                    "ward": jsonData["ward"],
                }

                candidateBlockchain.addCandidateData(data)

                return jsonify(
                    {"result": True, "data": candidateBlockchain.chain[-1].toJson()}
                )
            else:
                return jsonify({"result": False, "error": "Incomplete Data"})

        else:
            return jsonify({"result": False, "error": "Invalid JSON Format"})

    except:
        return jsonify({"result": False, "error": "Some error occured"})
