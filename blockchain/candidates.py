from block.candidate import Candidate
import requests
from constants import peers


class Candidates:
    previousIndex: int = 0
    candidatesList: list[Candidate] = []

    def addCandidate(
        self, candidateId: int, candidateName: str, state: str, district: str, ward: int
    ):
        if len(self.candidatesList) == 0:
            self.candidatesList.append(
                Candidate(0, candidateId, candidateName, state, district, ward)
            )
        else:
            self.candidatesList.append(
                Candidate(
                    self.previousIndex + 1,
                    candidateId,
                    candidateName,
                    state,
                    district,
                    ward,
                )
            )
            self.previousIndex += 1

    def announceNewCandidate(self, candidate: Candidate):
        """
        A function to announce to the network a new candidate.
        """

        print("Annoucing New Candidate To Peers")

        if len(peers) == 0:
            print("no registered peers, returning...")
            return

        for peer in peers:
            url = "{}/addCandidate".format(peer)
            headers = {"Content-Type": "application/json"}
            res = requests.post(url=url, json=candidate.toJson(), headers=headers)

            print("Peer: ", peer)
            print("API Response ", res.text)
            if res.status_code == 200:
                jsonData = res.json()
                print("Resulst: ", jsonData["result"])

                if jsonData["result"] == True:
                    print("add candidate res is True")
                    # if jsonData["data"]["Length"] != len(self.chain):
                    #     # self.consensus()
                    #     print('Canidate Data is diff')
