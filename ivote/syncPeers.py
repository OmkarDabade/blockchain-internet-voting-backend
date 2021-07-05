from ivote import iVoteApp
from flask import request, jsonify
from constants import peers

# API to sync Peers
@iVoteApp.route("/syncPeers", methods=["GET", "POST"])
def syncPeers():
    """
    Node-to-Node API
    """
    print("/syncPeers Called")

    try:
        if request.method == "GET":
            return jsonify(
                {
                    "result": True,
                    "length": len(peers),
                    "peers": list(peers),
                    "api": "/syncPeers",
                    "url": request.url,
                }
            )
        else:
            print("DATA RECIEVED:", request.data)
            if request.is_json:
                jsonData = request.get_json()
                receivedPeers = jsonData["peers"]

                # print("URL:", request.url)
                # parsedUri = urlparse(request.url)
                # print("Parsed URL:", parsedUri)
                # currentNodeAddress = "{uri.scheme}://{uri.netloc}".format(uri=parsedUri)
                print("CURRENT NODE ADDRESS: ", request.host_url)

                if len(peers) != len(receivedPeers):
                    for peer in receivedPeers:
                        if request.host_url != peer:
                            peers.add(str(peer))

                    print("adding peers done")
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncPeers",
                                "message": "Successfully Added All Peers",
                                "length": len(peers),
                                "url": request.url,
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {
                                "result": True,
                                "api": "/syncPeers",
                                "message": "Peers Already in Sync",
                                "length": len(peers),
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
                        "api": "/syncPeers",
                        "url": request.url,
                    }
                )

    except AttributeError:
        return jsonify(
            {
                "result": False,
                "message": "Provide data in json format",
                "api": "/syncPeers",
                "url": request.url,
            }
        )

    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncPeers",
                "url": request.url,
            }
        )
