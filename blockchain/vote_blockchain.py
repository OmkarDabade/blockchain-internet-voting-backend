from block.vote_block import VoteBlock
from constants import genesisBlockHash, difficultyVoteBlockchain, peers
import requests

# from blockchain import peers


class VoteBlockchain:
    """
    Blockchain class to store votes
    """

    def __init__(self):
        self.previousIndex = 0
        self.previousHash = genesisBlockHash
        self.chain = []

    def addBlock(self, data):
        """
        A function that adds the block to the chain after verification.
        """

        if len(self.chain) == 0:
            newBlock = VoteBlock(
                0,
                data["voteTo"],
                data["voteFrom"],
                data["timestamp"],
                genesisBlockHash,
            )

            # if not self.isValidProof(newBlock, newBlock.blockHash):
            #     return False

            self.chain.append(newBlock)
            # self.previousIndex += 1
            self.previousHash = newBlock.blockHash
        else:
            newBlock = VoteBlock(
                self.previousIndex + 1,
                data["voteTo"],
                data["voteFrom"],
                data["timestamp"],
                self.previousHash,
            )

            # if self.previousHash != newBlock.previousHash:
            #     return False

            # if not self.isValidProof(newBlock, newBlock.blockHash):
            #     return False

            self.chain.append(newBlock)
            self.previousIndex += 1
            self.previousHash = newBlock.blockHash
            self.announceNewBlock(newBlock)

    def acceptNewAnnouncedBlock(self, block):
        """
        A function that adds the newly announced block to the chain after verification.
        """
        print("Accept New Anounced Block")

        if len(self.chain) == 0:
            print("Previous     HASH:", self.previousHash)
            print("Recived BlockHASH:", block.previousBlockHash)

            if self.previousHash != block.previousBlockHash:
                print("Hash doesnt match")
                return False

            if not self.isValidProof(block, block.blockHash):
                print("is not valid proof")
                return False
        else:

            print("Previous     HASH:", self.previousHash)
            print("Recived BlockHASH:", block.previousBlockHash)

            if self.previousHash != block.previousBlockHash:
                print("Hash doesnt match")
                return False

            if not self.isValidProof(block, block.blockHash):
                print("is not valid proof")
                return False

        print("Block added to chain")
        self.chain.append(block)
        self.previousIndex += 1
        self.previousHash = block.blockHash
        return True

    @classmethod
    def isValidProof(cls, block, blockHash):
        """
        Check if blockHash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (
            blockHash.startswith("0" * difficultyVoteBlockchain)
            and blockHash == block.computeHash()
        )

    @classmethod
    def checkChainValidity(cls, chainDump):
        result = True
        previousHash = genesisBlockHash

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

            if (
                not cls.isValidProof(block, block.blockHash)
                or previousHash != block.previousBlockHash
            ):
                result = False
                break

            previousHash = block.blockHash

        return result

    def announceNewBlock(self, block):
        """
        A function to announce to the network once a block has been mined.
        Other blocks can simply verify the proof of work and add it to their
        respective chains.
        """
        print("Annoucing New Block To Peers")

        if len(peers) == 0:
            print("no registered peers, returning...")
            return

        for peer in peers:
            url = "{}/add_block".format(peer)
            headers = {"Content-Type": "application/json"}
            res = requests.post(url=url, json=block.toJson(), headers=headers)
            print("Peer: ", peer)
            print("API Response ", res.text)
            if res.status_code == 200:
                jsonData = res.json()
                print("Resulst: ", jsonData["result"])

                if jsonData["result"] == True:
                    print("res is True")
                    if jsonData["data"]["Length"] != len(self.chain):
                        self.consensus()

    def consensus(self):
        """
        Our naive consnsus algorithm. If a longer valid chain is
        found, our chain is replaced with it.
        """

        print("consensous called")
        longestChain = None
        current_len = len(self.chain)

        for node in peers:
            print(node)
            response = requests.get("{}/chain".format(node))
            length = response.json()["Length"]
            chain = response.json()["Chain"]
            if length > current_len and self.checkChainValidity(chain):
                current_len = length
                longestChain = chain

        if longestChain:
            self.chain = longestChain
            print("NewChain:", longestChain)
            return True

        return False


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
# @app.route("/add_block", methods=["POST"])
# def verify_and_add_block():
#     block_data = request.get_json()
#     block = Block(
#         block_data["index"],
#         block_data["transactions"],
#         block_data["timestamp"],
#         block_data["previous_hash"],
#         block_data["nonce"],
#     )

#     proof = block_data["hash"]
#     added = blockchain.add_block(block, proof)

#     if not added:
#         return "The block was discarded by the node", 400

#     return "Block added to the chain", 201


# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
# @app.route("/new_transaction", methods=["POST"])
# def new_transaction():
#     tx_data = request.get_json()
#     required_fields = ["author", "content"]

#     for field in required_fields:
#         if not tx_data.get(field):
#             return "Invalid transaction data", 404

#     tx_data["timestamp"] = time.time()

#     blockchain.add_new_transaction(tx_data)

#     return "Success", 201


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
# @app.route("/mine", methods=["GET"])
# def mine_unconfirmed_transactions():
#     result = blockchain.mine()
#     if not result:
#         return "No transactions to mine"
#     else:
#         # Making sure we have the longest chain before announcing to the network
#         chain_length = len(blockchain.chain)
#         consensus()
#         if chain_length == len(blockchain.chain):
#             # announce the recently mined block to the network
#             announce_new_block(blockchain.last_block)
#         return "Block #{} is mined.".format(blockchain.last_block.index)


# class Blockchain:
# difficulty of our PoW algorithm
# difficulty = 2

# def __init__(self):
#     self.unconfirmed_transactions = []
#     self.chain = []

# def create_genesis_block(self):
#     """
#     A function to generate genesis block and appends it to
#     the chain. The block has index 0, previous_hash as 0, and
#     a valid hash.
#     """
#     genesis_block = Block(0, [], 0, "0")
#     genesis_block.hash = genesis_block.compute_hash()
#     self.chain.append(genesis_block)

# @property
# def last_block(self):
#     return self.chain[-1]

# @staticmethod
# def proof_of_work(block):
#     """
#     Function that tries different values of nonce to get a hash
#     that satisfies our difficulty criteria.
#     """
#     block.nonce = 0

#     computed_hash = block.compute_hash()
#     while not computed_hash.startswith("0" * Blockchain.difficulty):
#         block.nonce += 1
#         computed_hash = block.compute_hash()

#     return computed_hash

# def add_new_transaction(self, transaction):
#     self.unconfirmed_transactions.append(transaction)

# def mine(self):
#     """
#     This function serves as an interface to add the pending
#     transactions to the blockchain by adding them to the block
#     and figuring out Proof Of Work.
#     """
#     if not self.unconfirmed_transactions:
#         return False

#     last_block = self.last_block

#     new_block = Block(
#         index=last_block.index + 1,
#         transactions=self.unconfirmed_transactions,
#         timestamp=time.time(),
#         previous_hash=last_block.hash,
#     )

#     proof = self.proof_of_work(new_block)
#     self.add_block(new_block, proof)

#     self.unconfirmed_transactions = []

#     return True
