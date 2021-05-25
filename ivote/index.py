from ivote import iVoteApp


@iVoteApp.route("/", methods=["GET"])
# @auth.login_required
def index():
    return "Hello World this is I-Vote Server"
