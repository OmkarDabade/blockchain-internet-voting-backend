from block.candidate import Candidate
import requests
from constants import POST_HEADERS, peers


class Candidates:
    # previousIndex: int = 0
    candidatesList: list[Candidate] = []

    def addCandidate(
        self, candidateId: int, candidateName: str, state: str, district: str, ward: int
    ):
        if len(self.candidatesList) == 0:
            self.candidatesList.append(
                Candidate(candidateId, candidateName, state, district, ward)
            )
        else:
            self.candidatesList.append(
                Candidate(
                    candidateId,
                    candidateName,
                    state,
                    district,
                    ward,
                )
            )
            # self.previousIndex += 1

    def announceNewCandidate(self, candidate: Candidate):
        """
        A function to announce to the network a new candidate.
        """
        print("Annoucing New Candidate To Peers")

        if len(peers) == 0:
            print("no registered peers, returning...")
            return

        for peer in peers:
            url = "{}addCandidate".format(peer)
            res = requests.post(url=url, json=candidate.toJson(), headers=POST_HEADERS)

            print("Peer: ", peer)
            print("API Response ", res.text)
            if res.status_code == 200:
                jsonData = res.json()
                print("Result: ", jsonData["result"])

                if jsonData["result"] == True:
                    print("add candidate res is True")
                    # if jsonData["data"]["Length"] != len(self.chain):
                    #     # self.consensus()
                    #     print('Canidate Data is diff')

    def getAllCandidatesInJson(self):
        candidateListInJson = []
        for candidate in self.candidatesList:
            candidateListInJson.append(candidate.toJson())

        return candidateListInJson
