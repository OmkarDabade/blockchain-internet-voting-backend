from database.model import Voter
from ivote import iVoteApp, voterDb
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


@iVoteApp.route("/addVoter", methods=["POST"])
def signup():
    """
    Node-to-Node API\n
    Authority-to-Node API
    """

    print("/addVoter Called")
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
                    mobile=jsonData["mobile"],
                    passwordHash=generate_password_hash(jsonData["password"]),
                )
                print("adding data")
                # insert user
                added = voterDb.addVoter(voter)
                if added:
                    print("adding done")
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/addVoter",
                                "result": "Successful Registration",
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    print("Could not Add User")
                    return jsonify(
                        {
                            "result": False,
                            "api": "/addVoter",
                            "error": "Registration Failed in Database",
                            "url": request.url,
                        }
                    )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/addVoter",
                    "url": request.url,
                }
            )

    except IntegrityError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "error": "Voter Db Rollback\nUser already exists",
                "api": "/addVoter",
                "url": request.url,
            }
        )
    except AttributeError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "error": "Provide data in json format",
                "api": "/addVoter",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/addVoter",
                "url": request.url,
            }
        )
