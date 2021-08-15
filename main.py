from ivote import iVoteApp
from blockchain import blockchain


if __name__ == "__main__":

    # Test Data
    for i in range(5):
        blockchain.addBlock(
            100 + i,
            f"Candidate Name %s" % (i + 1),
            f"Voter Id %s" % (i + 1),
        )

    for vote in blockchain.chain:
        print(vote)

    iVoteApp.run()
