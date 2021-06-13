from ivote.model import Voter
from flask_jwt_extended.utils import create_access_token
from ivote import iVoteApp, voterDb
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


@iVoteApp.route("/signup", methods=["POST"])
def signup():
    print("/signup Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            if (
                "voterId" in jsonData
                and "name" in jsonData
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
                voterDb.session.add(voter)
                voterDb.session.commit()
                print("adding done")

                # access_token = create_access_token(identity=voter.voterId)

                return (
                    jsonify(
                        {
                            "result": True,
                            "api": "/signup",
                            "result": "Successful Registration",
                            # "token": access_token,
                            "url": request.url,
                        }
                    ),
                    200,
                )

            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/signup",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/signup",
                    "url": request.url,
                }
            )

    except IntegrityError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "error": "Voter Db Rollback\nUser already exists",
                "api": "/signup",
                "url": request.url,
            }
        )
    except AttributeError:
        voterDb.session.rollback()
        return jsonify(
            {
                "result": False,
                "error": "Provide data in json format",
                "api": "/signup",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/signup",
                "url": request.url,
            }
        )