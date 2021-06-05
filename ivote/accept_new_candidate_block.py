# from block.candidate_block import CandidateBlock
# from ivote import chain, iVoteApp
# from flask import request, jsonify
# from blockchain import voteBlockchain


# @iVoteApp.route("/accept_new_candidate_block", methods=["POST"])
# def accept_new_candidate_block():
#     try:
#         if request.is_json:
#             jsonData = request.get_json()
#             print(jsonData)

#             if (
#                 "Block#" in jsonData
#                 and "Candidate Id" in jsonData
#                 and "Candidate Name" in jsonData
#                 and "State" in jsonData
#                 and "District" in jsonData
#                 and "Ward#" in jsonData
#                 and "Time" in jsonData
#                 and "Nonce" in jsonData
#                 and "Block Hash" in jsonData
#                 and "Previous Hash" in jsonData
#             ):
#                 newBlock = CandidateBlock(
#                     jsonData["Block#"],
#                     jsonData["Candidate Id"],
#                     jsonData["Candidate Name"],
#                     jsonData["State"],
#                     jsonData["District"],
#                     jsonData["Ward#"],
#                     jsonData["Time"],
#                     jsonData["Previous Hash"],
#                     jsonData["Block Hash"],
#                     jsonData["Nonce"],
#                 )

#                 voteBlockchain.addBlock(newBlock)
#                 chain()
#                 # return jsonify(
#                 #     {"result": True, "data": voteBlockchain.chain[-1].toJson()}
#                 # )
#             else:
#                 return jsonify({"result": False, "error": "Incomplete Data"})

#         else:
#             return jsonify({"result": False, "error": "Invalid JSON Format"})

#     except:
#         return jsonify({"result": False, "error": "Some error occured"})
