from ivote import iVoteApp
from flask import request, jsonify


@iVoteApp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.is_json:
            jsonData = request.get_json()
            print(jsonData)

            if "login" in jsonData and "password" in jsonData:
                print("Data Here")
                return jsonify({"result": True})

            else:
                return jsonify({"result": False, "error": "Incomplete Data"})

        else:
            return jsonify({"result": False, "error": "Invalid JSON Format"})
    except:
        return jsonify({"result": False, "error": "Some error occured"})
