from block.candidate_block import CandidateBlock


class CandidateBlockchain:
    previousIndex = 0
    previousHash = None
    chain = []

    def addCandidateData(self, data):
        self.chain.append(
            CandidateBlock(
                self.previousIndex + 1,
                data["candidateName"],
                data["candidateId"],
                data["candidateAgenda"],
                self.previousHash,
            )
        )
        self.previousIndex += 1
        self.previousHash = self.chain[-1].blockHash

    # def mine(self):
    #     pass
