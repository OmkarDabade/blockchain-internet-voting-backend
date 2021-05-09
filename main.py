from vote_blockchain import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)

blockchain = Blockchain()
blockchain.createGenesisBlock()
data = {}
data["voteTo"] = "Me"
data["timestamp"] = "now"


for i in range(5):
    data["voteFrom"] = f"Data Index %s" % (i + 1)
    blockchain.addBlock(data)

for item in blockchain.blockchain:
    print(item)

# for item in blockchain.blockchain:
#     print(item.blockHash == item.computeHash())

# for i in range(1,len(blockchain.blockchain)):
#     if(blockchain.blockchain[i-1].blockHash == blockchain.blockchain[i].previousBlockHash) and (blockchain.blockchain[i-1].index+1 == blockchain.blockchain[i].index):
#         print('TRUE')


# print(blockchain.blockchain[-1])


@app.route("/chain")
def getChain():
    chain = []
    for item in blockchain.blockchain:
        chain.append(item.toJson())

    return jsonify({"votedChain": chain})


@app.route("/")
def index():
    return "Hello World this is I-Vote Server"


if __name__ == "__main__":
    app.run(debug=True)
