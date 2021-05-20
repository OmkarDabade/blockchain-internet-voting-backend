from ivote import iVoteApp
from flask import request
from blockchain import voteBlockchain


@iVoteApp.route("/search/<string:key1>")
def search(key1):
    # query = request.get_json()
    print(key1)
    for item in voteBlockchain.chain:
        print(item.blockHash)
        if item.blockHash == key1:
            return item.toJson()

    return "NOT FOUND"
