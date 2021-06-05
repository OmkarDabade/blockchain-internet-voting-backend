# from blockchain import peers
from ivote import iVoteApp, get_chain
from flask import request, jsonify
import requests
from constants import peers

# import json

# endpoint to add new peers to the network.
@iVoteApp.route("/register_from_new_node", methods=["POST"])
def register_from_new_node():
    print("/register_from_new_node Called")
    try:
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)

            node_address = jsonData["node_address"]

            if not node_address:
                return jsonify(
                    {
                        "result": False,
                        "error": "Node Address not avialable in request",
                        "api": "/register_from_new_node",
                        "url": request.url,
                    }
                )

            # Add the node to the peer list
            peers.add(node_address)

            data = get_chain()
            print(data)
            header = {"Content-Type": "application/json"}

            # Make a request to register with remote node and send information
            res = requests.post(
                url=node_address + "/create_chain_from_dump",
                json=data,
                headers=header,
            )

            print(
                "Result After Making Post request create_chain_from_dump:",
                res.text,
            )

            return jsonify(
                {
                    "result": True,
                    "data": "Registration Successful",
                    "api": "/register_from_new_node",
                    "url": request.url,
                }
            )
            # if response.json()["result"] == "True":
            #     return jsonify({"result": True, "data": "Registration Successful"})
            # else:
            #     return jsonify({"result": False, "error": "unknown Error Occured"})

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/register_from_new_node",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/register_from_new_node",
                "url": request.url,
            }
        )

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
