from hashlib import sha256
import json

# class Block:
#     index = 0
#     data = None
#     blockHash = None
#     nonce = 0
#     previousBlockHash = None

#     def __init__(self,index,data,previousHash):
#         self.index = index
#         self.data = data
#         # self.blockHash = self.computeHash()
#         # self.nonce = nonce
#         self.previousBlockHash = previousHash
#         self.computeProofOfWork()

#     def computeHash(self):
#         # blockString = json.dumps(self.__dict__, sort_keys=True)
#         blockString = str(self.index) + str(self.data) + str(self.nonce) + str(self.previousBlockHash)
#         return sha256(blockString.encode()).hexdigest()
    
#     def computeProofOfWork(self):
#         self.nonce = 0
#         computedHash = self.computeHash()
#         while not computedHash.startswith('0' * 2):
#             self.nonce +=1
#             computedHash = self.computeHash()
#         self.blockHash = computedHash

#         # return blockHash
    
#     def __str__(self):
#         return '\nBlock#: %s\nData: %s\nNonce: %s\nHash: %s\nPrevious Hash: %s' %(self.index,self.data,self.nonce,self.blockHash,self.previousBlockHash)


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()