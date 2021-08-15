# class Candidate:
#     """
#     To Store Candidate Data
#     """

#     def __init__(
#         self,
#         candidateId: int,
#         candidateName: str,
#         state: str,
#         district: str,
#         ward: int,
#     ):
#         self.candidateName = candidateName
#         self.candidateId = candidateId
#         self.state = state
#         self.district = district
#         self.ward = ward

#     def __str__(self):
#         return (
#             "\nCandidate Id: %s\nCandidate Name: %s\nState: %s\nDistrict: %s\nWard#: %s"
#             % (
#                 self.candidateId,
#                 self.candidateName,
#                 self.state,
#                 self.district,
#                 self.ward,
#             )
#         )

#     def toJson(self):
#         return {
#             "candidateId": self.candidateId,
#             "candidateName": self.candidateName,
#             "state": self.state,
#             "district": self.district,
#             "ward": self.ward,
#         }

#     @staticmethod
#     def fromJson(jsonData: dict):
#         return Candidate(
#             jsonData["candidateId"],
#             jsonData["candidateName"],
#             jsonData["state"],
#             jsonData["district"],
#             jsonData["ward"],
#         )
