from block.candidate_block import CandidateBlock


class CandidateBlockchain:
    previousIndex = 0
    previousHash = None
    chain = []

    def addCandidateData(self, data):
        if len(self.chain) == 0:
            self.chain.append(
                CandidateBlock(
                    0,
                    data["candidateName"],
                    data["candidateId"],
                    data["state"],
                    data["district"],
                    data["ward"],
                    "GenesisBlock",
                )
            )
        else:
            self.chain.append(
                CandidateBlock(
                    self.previousIndex + 1,
                    data["candidateName"],
                    data["candidateId"],
                    data["state"],
                    data["district"],
                    data["ward"],
                    self.previousHash,
                )
            )
            self.previousIndex += 1
        self.previousHash = self.chain[-1].blockHash

    # def mine(self):
    #     pass
