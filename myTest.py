from datetime import datetime
import requests

baseUrl = "http://127.0.0.1:7457"
endpoint = "/castVote"
headers = {"Content-Type": "application/json"}
jsonData = {
    "candidateId": "MyCID",
    "candidateName": "NAME11",
    "voterId": 00,
    "district": 123,
    "ward": 1,
}

url = baseUrl + endpoint
# print(url)

# r = requests.post(url=url, json=jsonData, headers=headers)

# print("Response is:", r.json())
# print(type(r.json()["result"]))

addCandidate = {
    "candidateId": 1234,
    "candidateName": "Candidate Name 1",
    "state": "KA",
    "district": "BGM",
    "ward": 4,
}

castVote = {
    "candidateId": 789,
    "candidateName": "Casted Candidate",
    "fromVoter": "kjashvuishgvuiwlavysqlgvidbdbrsagyv",
}

getCandidate = {"state": "KA", "district": "BGM", "ward": 4}

login = {
    "voterId": "VoterId",
    "password": "TestPass",
}

nodeRegister = {
    "nodeAddress": "127.0.0.1:8000",
}

search = {
    "blockHash": 12,
    "blockNo": 45,
    "fromVoter": 45,
}

signUp = {
    "voterId": "VoterId",
    "name": "Voter Name",
    "mobile": 132456789,
    "password": "TestPass",
}
