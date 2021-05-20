from block.vote_block import VoteBlock


class VoteBlockchain:
    previousIndex = 0
    previousHash = None
    chain = []

    def addBlock(self, data):
        self.chain.append(
            VoteBlock(
                self.previousIndex + 1,
                data["voteTo"],
                data["voteFrom"],
                data["timestamp"],
                self.previousHash,
            )
        )
        self.previousIndex += 1
        self.previousHash = self.chain[-1].blockHash

    def createGenesisBlock(self, data=None):
        if data != None:
            self.chain.append(
                VoteBlock(
                    0,
                    data["voteTo"],
                    data["voteFrom"],
                    data["timestamp"],
                    "Previous Hash",
                )
            )
            # self.blockchain.append(VoteBlock(0, data, '0'))
        else:
            self.chain.append(
                VoteBlock(
                    0, "voteToCandidate", "voteFromVoter", "timestamp", "Previous Hash"
                )
            )
            # self.blockchain.append(VoteBlock(0, 'Genesis Block', '0'))
        self.previousIndex = 0
        self.previousHash = self.chain[-1].blockHash
