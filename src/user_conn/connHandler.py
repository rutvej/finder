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

# @conn_api.route("/matches",methods=["GET"])
# @token_validation
# def matches(username,role,user_id): 
#     try:
#         matches = User.query.fliter(UserConnections.user_name == username).all()
#         lis = [i[0] for i in matches]
#         res = User.query.filter(User.role != role,User.user_id.not_in(lis)).all()
#         return jsonify([r.to_json() for r in res])
#     except Exception as e:
#         print(e)
#         return {"error":"data not found"} ,400
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
        filename = username+"."+files.filename.split('.')[1]
        try:
            alread = repo.get_contents(filename)
            repo.update_file(filename,"update"+username,files.read(),alread.sha)
        except:
            repo.create_file(filename,"adding new file",files.read())
        u = User.query.filter(User.user_id == user_id).first()
        u.docs = "https://raw.githubusercontent.com/rutvej/images/main/"+filename
        db.session.add(u)
        db.session.commit()
        return {"status":"ok","url":"https://raw.githubusercontent.com/rutvej/images/main/"+filename}
    except Exception as e:
        print(e)
        return {"error":str(e)} ,400




@conn_api.route("/reset/<table>",methods=["POST"])
def reset_table(table):
    try:
        db.session.execute('''TRUNCATE TABLE {}'''.format(table))
        db.session.commit()
        return {"status":"ok"}
    except Exception as e:
        print(e)
        return {"error":str(e)} ,400