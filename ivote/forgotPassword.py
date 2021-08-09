from blockchain import blockchain
from database import adminDb

# from database.adminModel import Admin
# from database.voterModel import Voter
from ivote import iVoteApp, voterDb
from flask import request, jsonify


# API to change password in system(for voter as well as admin)
@iVoteApp.route("/forgotPassword", methods=["POST"])
def forgotPassword():
    """
    Client-to-Node API
    """
    print("/forgotPassword Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if (
                "voterId" in jsonData
                and "district" in jsonData
                and "name" in jsonData
                and "newPassword" in jsonData
            ):
                changed, msg = voterDb.changePassword(
                    voterId=jsonData["loginId"],
                    name=jsonData["name"],
                    district=jsonData["district"],
                    newPassowrd=jsonData["newPassword"],
                )

                if changed:
                    print("password changed")
                    blockchain.consensus()
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/forgotPassword",
                                "message": msg,
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    print("Could not Change Voter's Password")
                    return jsonify(
                        {
                            "result": False,
                            "api": "/forgotPassword",
                            "message": msg,
                            "url": request.url,
                        }
                    )

            elif (
                "loginId" in jsonData
                and "name" in jsonData
                and "newPassword" in jsonData
            ):
                changed, msg = adminDb.changePassword(
                    name=jsonData["name"],
                    loginId=jsonData["loginId"],
                    newPassowrd=jsonData["newPassword"],
                )

                if changed:
                    blockchain.consensus()
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/forgotPassword",
                                "message": msg,
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    print("Could not Change Admin Password")
                    return jsonify(
                        {
                            "result": False,
                            "api": "/forgotPassword",
                            "message": msg,
                            "url": request.url,
                        }
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/forgotPassword",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/forgotPassword",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/forgotPassword",
                "url": request.url,
            }
        )
