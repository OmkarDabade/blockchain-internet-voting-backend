from ivote import iVoteApp
from flask import request, jsonify
import requests
from constants import peers, POST_HEADERS
from blockchain import blockchain, candidates
from database import adminDb, voterDb


@iVoteApp.route("/registerFromNewNode", methods=["POST"])
def registerFromNewNode():
    """
    Node-to-Node API
    """
    print("/registerFromNewNode Called")
    print("DATA RECIEVED:", request.data)

    # try:
    if request.is_json:
        jsonData = request.get_json()
        newNodeAddress = jsonData["newNodeAddress"]

        if newNodeAddress == None:
            return jsonify(
                {
                    "result": False,
                    "message": "Node Address not avialable in request",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )

        # chain = blockchain.getChainInJson()
        # admins = adminDb.getAllAdminsInJson()
        # voters = voterDb.getAllVotersInJson()
        # candidateListInJson = candidates.getAllCandidatesInJson()

        # newPeers: list = list(peers)
        # newPeers.append(request.host_url)

        # jsonData = {
        #     "result": True,
        #     "chain": chain,
        #     "peers": newPeers,
        #     "candidates": candidateListInJson,
        #     "voters": voters,
        #     "admins": admins,
        # }
        # # header = {"Content-Type": "application/json"}

        # Add the node to the peer list
        peers.add(str(newNodeAddress))

        # # Make a request to register with remote node and send information
        # res = requests.post(
        #     url="{}syncAllData".format(newNodeAddress),
        #     json=jsonData,
        #     headers=POST_HEADERS,
        # )
        # print("Result After Making Post req /syncAllData:", res.text)

        res = blockchain.consensus()

        if res:
            return jsonify(
                {
                    "result": True,
                    "message": "Registration Successful and Data Synced",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )
        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Data Sync Failed",
                    "api": "/registerFromNewNode",
                    "url": request.url,
                }
            )

    else:
        return jsonify(
            {
                "result": False,
                "message": "Invalid JSON Format",
                "api": "/registerFromNewNode",
                "url": request.url,
            }
        )
    # except:
    #     return jsonify(
    #         {
    #             "result": False,
    #             "error": "Some error occured",
    #             "api": "/registerFromNewNode",
    #             "url": request.url,
    #         }
    #     )

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    # requests.post()


# @iVoteApp.route("/register_with", methods=["POST"])
# def register_with_existing_node():
#     """
#     Internally calls the `register_node` endpoint to
#     register current node with the node specified in the
#     request, and sync the blockchain as well as peer data.
#     """
#     node_address = request.get_json()["node_address"]

#     print("Called register with")
#     print(request.get_json())

#     if not node_address:
#         return "Invalid data", 400

#     data = {"node_address": request.host_url}
#     headers = {"Content-Type": "application/json"}

#     # Make a request to register with remote node and obtain information
#     response = requests.post(
#         node_address + "/register_node", data=json.dumps(data), headers=headers
#     )

#     if response.status_code == 200:
#         global blockchain
#         global peers
#         # update chain and the peers
#         # chain_dump = response.json()["chain"]
#         # blockchain = create_chain_from_dump(chain_dump)
#         peers.update(response.json()["peers"])
#         return "Registration successful", 200
#     else:
#         # if something goes wrong, pass it on to the API response
#         return response.content, response.status_code
