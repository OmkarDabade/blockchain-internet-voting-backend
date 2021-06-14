from .model import Voter
from flask_jwt_extended.utils import create_access_token
from ivote import iVoteApp
from flask import request, jsonify
from werkzeug.security import check_password_hash


@iVoteApp.route("/login", methods=["GET", "POST"])
def login():
    print("/GET login Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if "voterId" in jsonData and "password" in jsonData:
                print("Data is Here")

                user = Voter.query.filter_by(voterId=jsonData["voterId"]).first()

                if not user:
                    return (
                        jsonify(
                            {
                                "result": False,
                                "api": "/login",
                                "error": "User not found",
                                "url": request.url,
                            }
                        ),
                        404,
                    )

                if check_password_hash(user.passwordHash, jsonData["password"]):

                    access_token = create_access_token(identity=jsonData["voterId"])

                    return jsonify(
                        {
                            "result": True,
                            "api": "/login",
                            "token": access_token,
                            "url": request.url,
                        }
                    )
                else:
                    return jsonify(
                        {
                            "result": False,
                            "api": "/login",
                            "error": "Wrong Password",
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


# @iVoteApp.route("/login", methods=["POST"])
# def login():
#     print("/POST login Called")
#     try:
#         if request.is_json:
#             jsonData = request.get_json()
#             print("JSON DATA RECIEVED:", jsonData)

#             if "login" in jsonData and "password" in jsonData:
#                 print("Data Here")

#                 username = request.json.get("login", None)
#                 password = request.json.get("password", None)

#                 if username != "test" or password != "test":
#                     return jsonify({"msg": "Bad username or password"}), 401

#                 access_token = create_access_token(identity=username)

#                 return jsonify(
#                     {
#                         "result": True,
#                         "api": "/login",
#                         "token": access_token,
#                         "url": request.url,
#                     }
#                 )

#             else:
#                 return jsonify(
#                     {
#                         "result": False,
#                         "error": "Incomplete Data",
#                         "api": "/login",
#                         "url": request.url,
#                     }
#                 )

#         else:
#             return jsonify(
#                 {
#                     "result": False,
#                     "error": "Invalid JSON Format",
#                     "api": "/login",
#                     "url": request.url,
#                 }
#             )
#     except:
#         return jsonify(
#             {
#                 "result": False,
#                 "error": "Some error occured",
#                 "api": "/login",
#                 "url": request.url,
#             }
#         )
