from vote_block import VoteBlock


class Blockchain:
    previousIndex = 0
    previousHash = None
    blockchain = []

    def addBlock(self, data):
        self.blockchain.append(
            VoteBlock(self.previousIndex+1, data['voteTo'], data['voteFrom'], data['timestamp'], self.previousHash))
        self.previousIndex += 1
        self.previousHash = self.blockchain[-1].blockHash

    # def mine(self):
    #     pass

    def createGenesisBlock(self, data=None):
        if data != None:
            VoteBlock(0, data['voteTo'], data['voteFrom'],
                      data['timestamp'], 'Previous Hash')
            # self.blockchain.append(VoteBlock(0, data, '0'))
        else:
            VoteBlock(0, 'voteToCandidate', 'voteFromVoter',
                      'timestamp', 'Previous Hash')
            # self.blockchain.append(VoteBlock(0, 'Genesis Block', '0'))
        self.previousIndex = 0
        self.previousHash = self.blockchain[-1].blockHash
