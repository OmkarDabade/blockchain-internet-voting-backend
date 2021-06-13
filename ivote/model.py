from . import voterDb


# Database ORMs
class Voter(voterDb.Model):
    id = voterDb.Column(voterDb.Integer, primary_key=True)
    voterId = voterDb.Column(voterDb.String(15), unique=True)
    name = voterDb.Column(voterDb.String(60))
    mobile = voterDb.Column(voterDb.Integer, unique=True)
    passwordHash = voterDb.Column(voterDb.String(150))
