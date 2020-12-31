from blockchain import Blockchain

blockchain = Blockchain()
blockchain.createGenesisBlock()

for i in range(5):
    blockchain.addBlock('Data Index %s' %(i+1))

for item in blockchain.blockchain:
    print(item)

# for item in blockchain.blockchain:
#     print(item.blockHash == item.computeHash())

# for i in range(1,len(blockchain.blockchain)):
#     if(blockchain.blockchain[i-1].blockHash == blockchain.blockchain[i].previousBlockHash) and (blockchain.blockchain[i-1].index+1 == blockchain.blockchain[i].index):
#         print('TRUE')


    
# print(blockchain.blockchain[-1])