from constants import ROLE_ADMIN, ROLE_VOTER
from flask_jwt_extended.utils import create_access_token
from ivote import iVoteApp
from database import voterDb, adminDb
from flask import request, jsonify
from werkzeug.security import check_password_hash

# API to login into system(for admin as well as voter)
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
                print("Voter Data recieved")
                voter = voterDb.getVoter(jsonData["voterId"])

                if voter == None:
                    return (
                        jsonify(
                            {
                                "result": False,
                                "api": "/login",
                                "message": "Voter not found",
                                "url": request.url,
                            }
                        ),
                        404,
                    )

                if check_password_hash(voter.passwordHash, jsonData["password"]):
                    claims = {
                        "role": ROLE_VOTER,
                        "id": voter.voterId,
                        "name": voter.name,
                    }
                    accessToken = create_access_token(
                        identity=voter.voterId, additional_claims=claims
                    )
                    return jsonify(
                        {
                            "result": True,
                            "api": "/login",
                            "message": "Successful Login",
                            "isVoteCasted": voter.isVoteCasted,
                            "token": accessToken,
                            "voter": voter.toJson(),
                            "url": request.url,
                        }
                    )
                else:
                    return jsonify(
                        {
                            "result": False,
                            "api": "/login",
                            "message": "Wrong Password",
                            "url": request.url,
                        }
                    )
            elif "loginId" in jsonData and "password" in jsonData:
                print("Admin Data recieved")
                admin = adminDb.getAdmin(jsonData["loginId"])

                if admin == None:
                    return (
                        jsonify(
                            {
                                "result": False,
                                "api": "/login",
                                "message": "Admin not found",
                                "url": request.url,
                            }
                        ),
                        404,
                    )

                if check_password_hash(admin.passwordHash, jsonData["password"]):
                    print("admin pass matched")
                    claims = {
                        "role": ROLE_ADMIN,
                        "id": admin.loginId,
                        "name": admin.name,
                    }
                    accessToken = create_access_token(
                        identity=admin.loginId, additional_claims=claims
                    )
                    # print("access token")
                    return jsonify(
                        {
                            "result": True,
                            "api": "/login",
                            "message": "Successful Login",
                            "name": admin.name,
                            "loginId": admin.loginId,
                            "token": accessToken,
                            "url": request.url,
                        }
                    )
                else:
                    return jsonify(
                        {
                            "result": False,
                            "api": "/login",
                            "message": "Wrong Password",
                            "url": request.url,
                        }
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/login",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/login",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/login",
                "url": request.url,
            }
        )
