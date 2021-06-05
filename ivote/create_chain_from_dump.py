# from ivote.chain import chain
from blockchain import voteBlockchain
from flask import request, jsonify
from block.vote_block import VoteBlock
from ivote import iVoteApp, get_chain


@iVoteApp.route("/create_chain_from_dump", methods=["POST"])
def create_chain_from_dump():
    print("/create_chain_from_dump Called")
    try:
        print(request.is_json)
        if request.is_json:
            jsonData = request.get_json()
            print("JSON DATA RECIEVED:", jsonData)
            chainDump = jsonData["Chain"]

            for block_data in chainDump:

                block = VoteBlock(
                    index=block_data["Block#"],
                    voteTo=block_data["Vote To"],
                    voteFrom=block_data["Vote From"],
                    timestamp=block_data["Time"],
                    previousHash=block_data["Previous Hash"],
                    blockHash=block_data["Block Hash"],
                    nonce=block_data["Nonce"],
                )
                print("Block#:", block.index)
                print(block)

                added = voteBlockchain.acceptNewAnnouncedBlock(block)
                if not added:
                    # raise Exception("The chain dump is tampered!!")
                    print("Block not added in chain")
                    return jsonify(
                        {
                            "result": False,
                            "error": "Block# %s Not Added to Chain" % str(block.index),
                            "api": "/create_chain_from_dump",
                            "url": request.url,
                        }
                    )

            print("Creation of New Chain From Dump Successful")
            print(get_chain())

            return jsonify(
                {
                    "result": True,
                    "data": "Creating blockchain from dump successful",
                    "api": "/create_chain_from_dump",
                    "url": request.url,
                }
            )

        else:
            return jsonify(
                {
                    "result": False,
                    "error": "Invalid JSON Format",
                    "api": "/create_chain_from_dump",
                    "url": request.url,
                }
            )
    except:
        return jsonify(
            {
                "result": False,
                "error": "Some error occured",
                "api": "/create_chain_from_dump",
                "url": request.url,
            }
        )
