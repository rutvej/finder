import jwt 
from flask import request
from functools import wraps



def token_validation(caller_func):
        @wraps(caller_func)
        def valid_user(*args, **kwargs):
            try:
                token = request.headers.get("auth")
                token = jwt.decode(token,key="secret",algorithms=["HS256"])
                kwargs["username"] = token.get("username","demo")
                kwargs["role"] = token.get("role")
                kwargs["user_id"] = token.get("user_id")
                print(kwargs)
                return caller_func(*args, **kwargs)
            except Exception as e:
                return {"error":str(e)}
        return valid_user
