from ivote import iVoteApp
from flask import request

# Very first page of our API 
@iVoteApp.route("/", methods=["GET"])
def index():
    print("/index Called")
    print("URL:", request.url)
    print("CURRENT NODE ADDRESS: ", request.host_url)

    return "Hello World this is I-Vote Server at {}".format(request.host_url), 200
