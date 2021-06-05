from ivote import iVoteApp


@iVoteApp.route("/", methods=["GET"])
# @auth.login_required
def index():
    print("/index Called")
    return "Hello World this is I-Vote Server"
