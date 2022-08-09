from pydoc import doc
from flask import Blueprint,request
from models.models import db , User
from jwt import encode,decode
from datetime import datetime
from utils.decorator import token_validation

user_api = Blueprint("user",__name__)

@user_api.route("/createUser",methods=["POST"])
def createUser():
    try:
        data = request.json
        u = User(user_name=data["username"],docs=data.get("docs","N/A"),role=data.get("role","candidate").upper())
        u.set_password(data["password"])
        db.session.add(u)
        db.session.commit()
        return {"status":"success"}
    except Exception as e:
        print(e)
        return {"error":"User Already Exist"},400

@user_api.route("/generateToken",methods=["POST"])
def login():
    try:
        data = request.json
        data["exp"] = int(datetime.now().strftime('%s'))+60*30
        u = User.query.filter_by(user_name=data["username"]).first()
        if u.check_password(data["password"]):
            del data["password"]
            data["role"] = u.role
            data["user_id"] = u.user_id
            print(data)
            token = encode(data,key="secret")
            return {"access_token":token,"docs_link":u.docs}
        else:
            return {"error":"Wrong Credentials"},400
    except Exception as e:
        print(e)
        return {"error":"Wrong Credentials"}
        
@user_api.route("/editUser",methods=["POST"])
@token_validation
def editUser(username,role,user_id):
    try:
        data = request.json
        u = User.query.filter(User.user_id == user_id).first()
        u.docs = data["url"] if data.get("url") else u.docs
        u.docs = data["username"] if data.get("username") else u.user_name
        db.session.add(u)
        db.session.commit()
        return {"status":"ok"}
    except Exception as e:
        print(e)
        return {"error":"failed"},400

@user_api.route("/resetPassword",methods=["POST"])
@token_validation
def editUser(username,role,user_id):
    try:
        data = request.json
        u = User.query.filter(User.user_id == user_id).first()
        u.set_password(data["password"])
        db.session.add(u)
        db.session.commit()
        return {"status":"ok"}
    except Exception as e:
        print(e)
        return {"error":"failed"},400





    