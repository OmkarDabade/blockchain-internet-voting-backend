from ivote import iVoteApp
from flask import jsonify, request


@iVoteApp.route("/cast_vote")
def castVote():
    query = request.get_json()
    print(query)
    return "Done"
