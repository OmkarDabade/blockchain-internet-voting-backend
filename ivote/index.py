from ivote import iVoteApp


@iVoteApp.route("/", methods=["GET"])
def index():
    print("/index Called")
    return "Hello World this is I-Vote Server", 200
