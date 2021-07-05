from constants import *
from functools import wraps
from .voterDatabase import VoterDatabase
from .adminDatabase import AdminDatabase
from flask import jsonify, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request

voterDb = VoterDatabase()
adminDb = AdminDatabase()

from .voterModel import Voter
from .adminModel import Admin

# Custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def adminRequired(api: str = ""):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claim = get_jwt()
            print("CLAIM:", claim)

            if claim["role"] == ROLE_ADMIN:
                return fn(*args, **kwargs)
            else:
                return (
                    jsonify(
                        {
                            "result": False,
                            "api": api,
                            "error": "Admins only!",
                            "url": request.url,
                        }
                    ),
                    403,
                )

        return decorator

    return wrapper
