from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from app import db




class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),nullable=False,unique=True)
    docs = db.Column(db.String(255),nullable=True)
    role = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(255),nullable=False)

    # user_conn = db.relationship("User_Connections",foreign_keys='User.user_id')
    # user_conn = db.relationship("User_Connections",foreign_keys='User.user_name')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        data = {
            "username":self.user_name,
            "docs":self.docs,
            "to_id":self.user_id
        }
        return data



class UserConnections(db.Model):
    Tid = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),db.ForeignKey("user.user_name"))
    action = db.Column(db.Boolean)
    to_id = db.Column(db.Integer)


