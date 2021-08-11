BLOCKCHAIN_DIFFICULTY: int = 3

GENESIS_BLOCKHASH: str = "GenesisBlockHash"

ROLE_ADMIN: str = "admin"
ROLE_VOTER: str = "voter"
CANDIDATES: str = "candidates"

POST_HEADERS: dict = {"Content-Type": "application/json"}

# the address to other participating members of the network
#: Format "http://127.0.0.1:5000/"
peers: set = set()

CONSENSOUS_AFTER_N_BLOCKS = 5

VERSION: float = 0.3
