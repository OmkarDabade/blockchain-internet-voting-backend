# from block.candidate import Candidate
# import requests
# from constants import POST_HEADERS, peers


# class Candidates:
#     """
#     Class to store list of candidates
#     """

#     candidatesList: list[Candidate] = []

#     def addCandidate(
#         self, candidateId: int, candidateName: str, state: str, district: str, ward: int
#     ):
#         """
#         Function to add candidate in list
#         """
#         if len(self.candidatesList) == 0:
#             self.candidatesList.append(
#                 Candidate(candidateId, candidateName, state, district, ward)
#             )
#         else:
#             self.candidatesList.append(
#                 Candidate(candidateId, candidateName, state, district, ward)
#             )

#     def announceNewCandidate(self, candidate: Candidate):
#         """
#         A function to announce to the network a new candidate.
#         """
#         print("Annoucing New Candidate To Peers")

#         if len(peers) == 0:
#             print("no registered peers, returning...")
#             return

#         for peer in peers:
#             url = "{}addCandidate".format(peer)
#             res = requests.post(url=url, json=candidate.toJson(), headers=POST_HEADERS)

#             print("Peer: ", peer)
#             print("API Response: ", res.text)

#     def getAllCandidatesInJson(self):
#         """
#         Function to return candidate list in JSON format
#         """
#         candidateListInJson = []
#         for candidate in self.candidatesList:
#             candidateListInJson.append(candidate.toJson())

#         return candidateListInJson
