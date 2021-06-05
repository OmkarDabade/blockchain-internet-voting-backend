from werkzeug.security import generate_password_hash

difficultyVoteBlockchain = 4
difficultyCandidateBlockchain = difficultyVoteBlockchain

genesisBlockHash = "GenesisBlockHash"

users = {
    "john": generate_password_hash("Test_Pass"),
    "susan": generate_password_hash("HI_THERE"),
}

# the address to other participating members of the network
peers = set()
