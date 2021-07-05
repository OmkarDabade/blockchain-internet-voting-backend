from block.candidate import Candidate
from database.voterModel import Voter
from database.adminModel import Admin
from blockchain import blockchain
from flask import request, jsonify
from ivote import iVoteApp
from constants import peers
from database import adminDb, voterDb
from blockchain import candidateList


@iVoteApp.route("/syncAllData", methods=["POST"])
def syncAllData():
    """
    Node-to-Node API
    """
    print("/syncAllData Called")
    print("DATA RECIEVED:", request.data)

    try:
        if request.is_json:
            jsonData = request.get_json()

            if "chain" in jsonData:
                chainDump = jsonData["chain"]
                if len(blockchain.chain) != len(chainDump):
                    added = blockchain.syncChain(chainDump)
                    if not added:
                        print("Chain Not Synced(or)Chain Tampered")
                    #     print("Chain is Tampered")
                    #     return jsonify(
                    #         {
                    #             "result": False,
                    #             "message": "Chain Not Synced(or)Chain Tampered",
                    #             "api": "/syncAllData",
                    #             "url": request.url,
                    #         }
                    #     )
                    print("Creation of New Chain From Dump Successful")

            if "peers" in jsonData:
                receivedPeers = jsonData["peers"]
                print("CURRENT NODE ADDRESS: ", request.host_url)

                if len(peers) != len(receivedPeers):
                    for peer in receivedPeers:
                        if request.host_url != peer:
                            peers.add(str(peer))

            if "candidates" in jsonData:
                receivedCandidates = jsonData["candidates"]
                if len(candidateList) != len(receivedCandidates):
                    for candidateData in receivedCandidates:
                        candidate = Candidate.fromJson(candidateData)
                        if candidate.candidateId not in candidateList:
                            candidateList.append(candidate)

            if "admins" in jsonData:
                receivedAdmins = jsonData["admins"]
                if adminDb.totalAdmins() != len(receivedAdmins):
                    for adminData in receivedAdmins:
                        newAdmin = Admin.fromJson(adminData)
                        admin = adminDb.getAdmin(newAdmin.loginId)

                        if admin == None:
                            adminDb.addAdmin(newAdmin)

            if "voters" in jsonData:
                receivedVoters = jsonData["voters"]
                if voterDb.totalVoters() != len(receivedVoters):
                    for voterData in receivedVoters:
                        newVoter = Voter.fromJson(voterData)
                        voter = voterDb.getVoter(newVoter.voterId)

                        if voter == None:
                            voterDb.addVoter(newVoter)

            return jsonify(
                {
                    "result": True,
                    "message": "Data Synced Successfully",
                    "api": "/syncAllData",
                    "url": request.url,
                }
            )

        else:
            return jsonify(
                {
                    "result": False,
                    "message": "Invalid JSON Format",
                    "api": "/syncAllData",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "message": "Some error occured",
                "api": "/syncAllData",
                "url": request.url,
            }
        )
