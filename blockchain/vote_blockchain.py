from block.vote_block import VoteBlock


class VoteBlockchain:
    previousIndex = 0
    previousHash = None
    chain = []

    def addBlock(self, data):
        if len(self.chain) == 0:
            self.chain.append(
                VoteBlock(
                    0,
                    data["voteTo"],
                    data["voteFrom"],
                    data["timestamp"],
                    "Genesis Block",
                )
            )
        else:
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
