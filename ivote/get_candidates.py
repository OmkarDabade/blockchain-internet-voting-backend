from ivote import iVoteApp
from flask import request, jsonify
from blockchain import candidateBlockchain


@iVoteApp.route("/get_candidates", methods=["GET"])
def get_candidates():
    print("/get_candidates Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)
            chain = []

            if "state" in jsonData and "district" in jsonData and "ward" in jsonData:
                print("Entered in 3")
                for item in candidateBlockchain.chain:
                    print("Entered Loop")
                    if (
                        item.state == jsonData["state"]
                        and item.district == jsonData["district"]
                        and item.ward == jsonData["ward"]
                    ):
                        print("Match found")
                        chain.append(item.toJson())

                return jsonify(
                    {
                        "result": True,
                        "data": chain,
                        "api": "/get_candidates",
                        "url": request.url,
                    }
                )

            elif "state" in jsonData and "district" in jsonData:
                for item in candidateBlockchain.chain:
                    if (
                        item.state == jsonData["state"]
                        and item.district == jsonData["district"]
                    ):
                        chain.append(item.toJson())

                return jsonify(
                    {
                        "result": True,
                        "data": chain,
                        "api": "/get_candidates",
                        "url": request.url,
                    }
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/get_candidates",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/get_candidates",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/get_candidates",
                "url": request.url,
            }
        )
