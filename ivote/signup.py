from blockchain import blockchain
from database import adminDb
from database.adminModel import Admin
from database.voterModel import Voter
from ivote import iVoteApp, voterDb
from flask import request, jsonify
from werkzeug.security import generate_password_hash

# API to register in system(for voter as well as admin)
@iVoteApp.route("/signup", methods=["POST"])
def signup():
    """
    Client-to-Authority API
    """
    print("/signup Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if (
                "voterId" in jsonData
                and "name" in jsonData
                and "state" in jsonData
                and "district" in jsonData
                and "ward" in jsonData
                and "mobile" in jsonData
                and "password" in jsonData
            ):
                voter = Voter(
                    voterId=jsonData["voterId"],
                    name=jsonData["name"],
                    state=jsonData["state"],
                    district=jsonData["district"],
                    ward=jsonData["ward"],
                    mobile=jsonData["mobile"],
                    passwordHash=generate_password_hash(jsonData["password"]),
                )
                print("adding voter")
                # insert user
                added, msg = voterDb.addVoter(voter)
                if added:
                    print("adding done")
                    blockchain.consensus()
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/signup",
                                "message": msg,
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    print("Could not Add Voter")
                    return jsonify(
                        {
                            "result": False,
                            "api": "/signup",
                            "message": msg,
                            "url": request.url,
                        }
                    )

            elif (
                "loginId" in jsonData and "name" in jsonData and "password" in jsonData
            ):
                admin = Admin(
                    loginId=jsonData["loginId"],
                    name=jsonData["name"],
                    passwordHash=generate_password_hash(jsonData["password"]),
                )
                print("adding admin")
                # insert admin
                added, msg = adminDb.addAdmin(admin)
                if added:
                    print("adding done")
                    blockchain.consensus()
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/signup",
                                "message": msg,
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    print("Could not Add Admin")
                    return jsonify(
                        {
                            "result": False,
                            "api": "/signup",
                            "message": msg,
                            "url": request.url,
                        }
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/signup",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/signup",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/signup",
                "url": request.url,
            }
        )
