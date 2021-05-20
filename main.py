from ivote import iVoteApp
from blockchain import voteBlockchain


data = {}
data["voteTo"] = "Me"
data["timestamp"] = "now"


if __name__ == "__main__":

    voteBlockchain.createGenesisBlock()

    # Test Data
    for i in range(5):
        data["voteFrom"] = f"Data Index %s" % (i + 1)
        voteBlockchain.addBlock(data)

    for item in voteBlockchain.chain:
        print(item)

    iVoteApp.run(debug=True)


# for item in blockchain.blockchain:
#     print(item)

# for item in blockchain.blockchain:
#     print(item.blockHash == item.computeHash())

# for i in range(1,len(blockchain.blockchain)):
#     if(blockchain.blockchain[i-1].blockHash == blockchain.blockchain[i].previousBlockHash) and (blockchain.blockchain[i-1].index+1 == blockchain.blockchain[i].index):
#         print('TRUE')


# print(blockchain.blockchain[-1])
