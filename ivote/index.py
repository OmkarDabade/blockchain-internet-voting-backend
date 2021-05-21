from ivote import iVoteApp


@iVoteApp.route("/", methods=['GET'])
def index():
    return "Hello World this is I-Vote Server"
