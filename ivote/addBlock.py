from block.vote import Vote
from ivote import iVoteApp
from ivote.chain import get_chain
from flask import request, jsonify
from blockchain import blockchain


@iVoteApp.route("/addBlock", methods=["POST"])
def addBlock():
    """
    Node-to-Node API
    """

    print("/addBlock Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if (
                "block#" in jsonData
                and "candidateId" in jsonData
                and "candidateName" in jsonData
                and "fromVoter" in jsonData
                and "time" in jsonData
                and "nonce" in jsonData
                and "blockHash" in jsonData
                and "previousHash" in jsonData
            ):
                newBlock = Vote(
                    jsonData["block#"],
                    jsonData["candidateId"],
                    jsonData["candidateName"],
                    jsonData["fromVoter"],
                    jsonData["time"],
                    jsonData["previousHash"],
                    blockHash=jsonData["blockHash"],
                    nonce=jsonData["nonce"],
                )

                res = blockchain.acceptNewAnnouncedBlock(newBlock)

                if res:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "data": get_chain(),
                                "api": "/addBlock",
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    return jsonify(
                        {
                            "result": False,
                            "error": "Block Not Added to chain",
                            "api": "/addBlock",
                            "url": request.url,
                        }
                    )
            else:
                return jsonify(
                    {
                        "result": False,
                        "error": "Incomplete Data",
                        "api": "/addBlock",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/addBlock",
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
