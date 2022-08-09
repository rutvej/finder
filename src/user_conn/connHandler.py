from flask import Blueprint,request,jsonify
import github
from models.models import db , User , UserConnections
from jwt import encode,decode
from datetime import datetime
from utils.decorator import token_validation
from github import Github
from uuid import uuid4
import os

conn_api = Blueprint("user_con",__name__)

        
@conn_api.route("/Showlist",methods=["GET"])
@token_validation
def showlist(username,role,user_id): 
    try:
        swipe = db.session.query(UserConnections.to_id).filter(UserConnections.user_name == username,UserConnections.action == True).distinct().all()
        lis = [i[0] for i in swipe]
        res = User.query.filter(User.role != role,User.user_id.not_in(lis)).all()
        return jsonify([r.to_json() for r in res])
    except Exception as e:
        print(e)
        return {"error":"data not found"} ,400

@conn_api.route("/action/<action>",methods=["POST"])
@token_validation
def user_action(username,role,user_id,action):
    try:
        data = request.json
        check = UserConnections.query.filter(UserConnections.user_name == data["username"],UserConnections.to_id == user_id,).all()
        action_data= UserConnections(user_name=username,
                                    action= True if action == "right" else False,
                                    to_id=data["to_id"]) 
        
        db.session.add(action_data)
        db.session.commit()
        if check != []:
            return {"status":"match"}
        return {"status":"ok"}
    except Exception as e:
        print(e)
        return {"error":"Already Swipe " + action} ,400

@conn_api.route("/fileupload",methods=["POST"])
@token_validation
def fileupload(username,role,user_id):
    try:
        files = request.files["file"]
        github = Github(os.getenv("GITKEY"))
        repo = github.get_user().get_repo("images")
        filename = files.filename.split('.')
        try:
            alread = repo.get_contents(username+filename[1])
            repo.update_file(username+filename[1],"update"+username,files.read(),alread.sha)
        except:
            repo.create_file(username+filename[1],"adding new file",files.read())
        return {"status":"ok","url":"https://raw.githubusercontent.com/rutvej/images/main/"+username+filename[1]}
    except Exception as e:
        print(e)
        return {"error":str(e)} ,400





    