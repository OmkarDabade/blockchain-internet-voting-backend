from ivote import iVoteApp


@iVoteApp.route("/")
def index():
    return "Hello World this is I-Vote Server"
