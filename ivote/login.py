from constants import ROLEADMIN, ROLEVOTER
from flask_jwt_extended.utils import create_access_token
from ivote import iVoteApp
from database import voterDb, adminDb
from flask import request, jsonify
from werkzeug.security import check_password_hash


@iVoteApp.route("/login", methods=["GET", "POST"])
def login():
    """
    Client-to-Node API
    """

    print("/GET login Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if "voterId" in jsonData and "password" in jsonData:
                print("Voter Data is Here")

                # user = Voter.query.filter_by(voterId=jsonData["voterId"]).first()
                voter = voterDb.getVoter(jsonData["voterId"])

                if not voter:
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

                if check_password_hash(voter.passwordHash, jsonData["password"]):
                    add_claims = {
                        "role": ROLEVOTER,
                        "id": voter.voterId,
                        "name": voter.name,
                    }
                    access_token = create_access_token(
                        identity=jsonData["voterId"], additional_claims=add_claims
                    )
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
            elif "loginId" in jsonData and "password" in jsonData:
                print("Admin Data is Here")

                # user = Voter.query.filter_by(voterId=jsonData["voterId"]).first()
                admin = adminDb.getAdmin(jsonData["loginId"])
                print(admin)

                if not admin:
                    return (
                        jsonify(
                            {
                                "result": False,
                                "api": "/login",
                                "error": "Admin not found",
                                "url": request.url,
                            }
                        ),
                        404,
                    )

                if check_password_hash(admin.passwordHash, jsonData["password"]):
                    print("pass matched")
                    add_claims = {
                        "role": ROLEADMIN,
                        "id": admin.loginId,
                        "name": admin.name,
                    }
                    access_token = create_access_token(
                        identity=admin.loginId, additional_claims=add_claims
                    )
                    print("access token")
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
