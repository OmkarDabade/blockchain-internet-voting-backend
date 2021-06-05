from block.vote_block import VoteBlock
from ivote import iVoteApp, get_chain
from flask import request, jsonify
from blockchain import voteBlockchain

# from .chain import chain


@iVoteApp.route("/add_block", methods=["POST"])
def add_block():
    print("/add_block Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            if (
                "Block#" in jsonData
                and "Vote To" in jsonData
                and "Vote From" in jsonData
                and "Time" in jsonData
                and "Nonce" in jsonData
                and "Block Hash" in jsonData
                and "Previous Hash" in jsonData
            ):
                newBlock = VoteBlock(
                    jsonData["Block#"],
                    jsonData["Vote To"],
                    jsonData["Vote From"],
                    jsonData["Time"],
                    jsonData["Previous Hash"],
                    blockHash=jsonData["Block Hash"],
                    nonce=jsonData["Nonce"],
                )

                # voteBlockchain.addBlock(newBlock)
                res = voteBlockchain.acceptNewAnnouncedBlock(newBlock)
                # chain()
                if res:
                    return jsonify(
                        {
                            "result": True,
                            "data": get_chain(),
                            "api": "/add_block",
                            "url": request.url,
                        }
                    )
                else:
                    return jsonify(
                        {
                            "result": False,
                            "error": "Block Not Added to chain",
                            "api": "/add_block",
                            "url": request.url,
                        }
                    )
            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/add_block",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/add_block",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/add_block",
                "url": request.url,
            }
        )
