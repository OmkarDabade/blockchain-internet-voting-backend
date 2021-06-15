from blockchain import blockchain
from flask import request, jsonify
from block.vote import Vote
from ivote import iVoteApp, get_chain


@iVoteApp.route("/createChainFromDump", methods=["POST"])
def createChainFromDump():
    """
    Node-to-Node API
    """

    print("/createChainFromDump Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()
            chainDump = jsonData["Chain"]

            for block_data in chainDump:

                block = Vote(
                    index=block_data["block#"],
                    candidateId=block_data["candidateId"],
                    candidateName=block_data["candidateName"],
                    fromVoter=block_data["fromVoter"],
                    timestamp=block_data["time"],
                    previousHash=block_data["previousHash"],
                    blockHash=block_data["blockHash"],
                    nonce=block_data["nonce"],
                )
                print("Block#:", block.index)

                added = blockchain.acceptNewAnnouncedBlock(block)
                if not added:
                    # raise Exception("The chain dump is tampered!!")
                    print("Block not added in chain")
                    return jsonify(
                        {
                            "result": False,
                            "error": "Block# %s Not Added to Chain" % str(block.index),
                            "api": "/createChainFromDump",
                            "url": request.url,
                        }
                    )

            print("Creation of New Chain From Dump Successful")
            print(get_chain())

            return jsonify(
                {
                    "result": True,
                    "data": "Creating blockchain from dump successful",
                    "api": "/createChainFromDump",
                    "url": request.url,
                }
            )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/createChainFromDump",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/createChainFromDump",
                "url": request.url,
            }
        )
