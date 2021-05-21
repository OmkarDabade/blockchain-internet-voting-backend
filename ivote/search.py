from ivote import iVoteApp
from flask import request
from blockchain import voteBlockchain


@iVoteApp.route("/search", methods=["GET"])
def search():
    try:
        blockHash = request.args.get("blockHash")
        print(blockHash)

        for item in voteBlockchain.chain:
            print(item.blockHash)

        if item.blockHash == blockHash:
            return item.toJson()

    finally:
        return "NOT FOUND"
