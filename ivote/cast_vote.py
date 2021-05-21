from block.vote_block import VoteBlock
from ivote import iVoteApp
from flask import jsonify, request
from blockchain import voteBlockchain


@iVoteApp.route("/cast_vote", methods=["POST"])
def castVote():
    try:
        candidateId = request.args.get("candidateId")
        print(candidateId)

        voterId = request.args.get("voterId")
        print(voterId)

        if candidateId is not None:
            voteBlockchain.addBlock(
                {"voteTo": candidateId, "timestamp": "now", "voteFrom": voterId}
            )

        return jsonify(
            {
                "blockHash": voteBlockchain.chain[-1].blockHash,
            }
        )

    finally:
        return "NOT FOUND"
