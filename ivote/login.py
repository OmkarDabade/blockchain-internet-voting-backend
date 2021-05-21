from ivote import iVoteApp
from flask import request


@iVoteApp.route("/login", methods=["GET", "POST"])
def login():
    try:
        loginId = request.args.get("loginId")
        print(loginId)
        password = request.args.get("password")
        print(password)

    finally:
        return "USER NOT FOUND"
