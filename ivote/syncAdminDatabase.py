from database import Admin
from ivote import iVoteApp
from flask import request, jsonify
from database import adminDb

# API to sync Admin database
@iVoteApp.route("/syncAdminDatabase", methods=["GET", "POST"])
def syncAdminDatabase():
    """
    Node-to-Node API
    """
    print("/syncAdminDatabase Called")

    try:
        if request.method == "GET":
            return jsonify(
                {
                    "result": True,
                    "length": adminDb.totalAdmins(),
                    "admins": adminDb.getAllAdminsInJson(),
                    "api": "/syncAdminDatabase",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedAdmins = jsonData["admins"]

                if adminDb.totalAdmins() != len(receivedAdmins):
                    for adminData in receivedAdmins:
                        newAdmin = Admin.fromJson(adminData)
                        admin = adminDb.getAdmin(newAdmin.loginId)

                        if admin == None:
                            adminDb.addAdmin(newAdmin)

                    print("adding admins done")
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncAdminDatabase",
                                "message": "Successfully Synced VoterDb",
                                "length": adminDb.totalAdmins(),
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncAdminDatabase",
                                "message": "AdminDb Already in Sync",
                                "length": adminDb.totalAdmins(),
                                "url": request.url,
                            }
                        ),
                        200,
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Invalid JSON Format",
                        "api": "/syncAdminDatabase",
                        "url": request.url,
                    }
                )

    except AttributeError:
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/syncAdminDatabase",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncAdminDatabase",
                "url": request.url,
            }
        )
