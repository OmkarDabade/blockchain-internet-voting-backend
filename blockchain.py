from block import Block

class Blockchain:
    previousIndex = 0
    previousHash = None
    blockchain = []

    def addBlock(self,data):
        self.blockchain.append(Block(self.previousIndex+1,data,self.previousHash))
        self.previousIndex += 1
        self.previousHash = self.blockchain[-1].blockHash

    # def mine(self):
    #     pass

    def createGenesisBlock(self,data=None):
        if data != None:
            self.blockchain.append(Block(0,data,'0'))
        else:
            self.blockchain.append(Block(0,'Genesis Block','0'))
        self.previousIndex = 0
        self.previousHash = self.blockchain[-1].blockHash