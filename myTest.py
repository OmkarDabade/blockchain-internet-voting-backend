import requests

baseUrl = "http://127.0.0.1:8000"
endpoint = "/cast_vote"
headers = {"Content-Type": "application/json"}
jsonData = {
    "candidateId": "MyCID",
    "candidateName": "NAME11",
    "voterId": 00,
    "district": 123,
    "ward": 1,
}

url = baseUrl + endpoint
print(url)

r = requests.post(url=url, json=jsonData, headers=headers)

print("Response is:", r.json())
print(type(r.json()["result"]))
