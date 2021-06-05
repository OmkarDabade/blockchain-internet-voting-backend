from ivote import iVoteApp
from flask import request, jsonify


@iVoteApp.route("/login", methods=["GET", "POST"])
def login():
    print("/login Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            if "login" in jsonData and "password" in jsonData:
                print("Data Here")
                return jsonify(
                    {
                        "result": True,
                        "api": "/login",
                        "url": request.url,
                    }
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/login",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/login",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/login",
                "url": request.url,
            }
        )
