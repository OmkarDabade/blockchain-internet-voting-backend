from werkzeug.security import generate_password_hash

difficultyVoteBlockchain = 4
difficultyCandidateBlockchain = difficultyVoteBlockchain

users = {
    "john": generate_password_hash("Test_Pass"),
    "susan": generate_password_hash("HI_THERE"),
}
