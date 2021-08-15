from block.vote import Vote
from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain

# API to add newly announced block to chain
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
                newBlock = Vote.fromJson(jsonData)
                res = blockchain.acceptNewAnnouncedBlock(newBlock)

                if res:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "data": blockchain.getChainInJson(),
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
                            "message": "Block Not Added to chain",
                            "api": "/addBlock",
                            "url": request.url,
                        }
                    )
            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Incomplete Data",
                        "api": "/addBlock",
                        "url": request.url,
                    }
                )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/addBlock",
                    "url": request.url,
                }
            )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/addBlock",
                "url": request.url,
            }
        )
