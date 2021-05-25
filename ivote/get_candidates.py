from ivote import iVoteApp
from flask import request, jsonify
from blockchain import candidateBlockchain


@iVoteApp.route("/get_candidates", methods=["GET"])
def get_candidates():
    try:
        if request.is_json:
            jsonData = request.get_json()
            print(jsonData)
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

                return jsonify({"result": True, "data": chain})

            elif "state" in jsonData and "district" in jsonData:
                for item in candidateBlockchain.chain:
                    if (
                        item.state == jsonData["state"]
                        and item.district == jsonData["district"]
                    ):
                        chain.append(item.toJson())

                return jsonify({"result": True, "data": chain})

            else:
                return jsonify({"result": False, "error": "Incomplete Data"})

        else:
            return jsonify({"result": False, "error": "Invalid JSON Format"})

    except:
        return jsonify({"result": False, "error": "Some error occured"})
