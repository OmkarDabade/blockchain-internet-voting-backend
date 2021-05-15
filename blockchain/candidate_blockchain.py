from block.candidate_block import CandidateBlock


class CandidateBlockchain:
    previousIndex = 0
    previousHash = None
    blockchain = []

    def addCandidateData(self, data):
        self.blockchain.append(
            CandidateBlock(
                self.previousIndex + 1,
                data["candidateName"],
                data["candidateId"],
                data["candidateAgenda"],
                self.previousHash,
            )
        )
        self.previousIndex += 1
        self.previousHash = self.blockchain[-1].blockHash

    # def mine(self):
    #     pass
