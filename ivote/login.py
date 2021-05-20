from ivote import iVoteApp
from flask import jsonify, request


@iVoteApp.route("/login")
def login():
    # query = request.get_json()
    # print(query)
    return "Done"
