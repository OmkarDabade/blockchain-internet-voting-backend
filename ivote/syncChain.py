from ivote import iVoteApp
from flask import request, jsonify
from blockchain import blockchain

# API to sync chain
@iVoteApp.route("/syncChain", methods=["GET", "POST"])
def syncChain():
    """
    Node-to-Node API
    """
    print("/syncChain Called")

    try:
        if request.method == "GET":
            return jsonify(
                {
                    "result": True,
                    "length": len(blockchain.chain),
                    "chain": blockchain.getChainInJson(),
                    "api": "/syncChain",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedChainDump = jsonData["chain"]

                if len(blockchain.chain) != len(receivedChainDump):
                    added = blockchain.syncChain(receivedChainDump)
                    if added:
                        print("Successfully Synced Chain")
                        return (
                            jsonify(
                                {
                                    "result": True,
                                    "api": "/syncChain",
                                    "message": "Successfully Synced Chain",
                                    "length": len(blockchain.chain),
                                    "url": request.url,
                                }
                            ),
                            200,
                        )
                    else:
                        print("Chain Tampered and not synced")
                        return jsonify(
                            {
                                "result": False,
                                "api": "/syncChain",
                                "message": "Chain Tampered and not synced",
                                "length": len(blockchain.chain),
                                "url": request.url,
                            }
                        )
                else:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncChain",
                                "message": "Chain Already in Sync",
                                "length": len(blockchain.chain),
                                "url": request.url,
                            }
                        ),
                        200,
                    )

            else:
                return jsonify(
                    {
                        "result": False,
                        "message": "Invalid JSON Format",
                        "api": "/syncChain",
                        "url": request.url,
                    }
                )

    except AttributeError:
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/syncChain",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncChain",
                "url": request.url,
            }
        )
