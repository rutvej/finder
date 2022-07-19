from app import create_app,db
from user.handleUser import user_api
from user_conn.connHandler import conn_api


app = create_app()
db.create_all(app=app)
app.register_blueprint(user_api)
app.register_blueprint(conn_api)

if __name__ == "__main__":
    app.run(port=3003,debug=True)