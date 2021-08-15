from blockchain import blockchain
from database import adminRequired
from database.voterModel import Voter
from ivote import iVoteApp, voterDb
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

# API to add new voter to database
@iVoteApp.route("/addVoter", methods=["POST"])
@adminRequired(api="/addVoter")
def addVoter():
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
                and "passwordHash" in jsonData
                and "isVoteCasted" in jsonData
            ):
                voter = Voter.fromJson(jsonData)
                print("adding data")

                # insert user
                added, msg = voterDb.addVoter(voter)

                if added:
                    print("adding done")
                    blockchain.consensus()

                else:
                    print("Could not Add Voter")

                return (
                    jsonify(
                        {
                            "result": added,
                            "api": "/addVoter",
                            "message": msg,
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
                    "api": "/addVoter",
                    "url": request.url,
                }
            )

    except IntegrityError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "message": "Voter Db Rollback\nUser already exists",
                "api": "/addVoter",
                "url": request.url,
            }
        )
    except AttributeError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/addVoter",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/addVoter",
                "url": request.url,
            }
        )
