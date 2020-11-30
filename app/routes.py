from flask import request
from app import app
from app.database import create, read, update, delete, scan
from datetime import datetime



@app.route("/")
def index():
    serv_time = datetime.now().strftime("%F %H:%M:%S")
    return {
            "ok": True,
            "version": "1.0.0",
            "server_time":serv_time
            }



@app.route("/users")
def get_all_users():
    out = scan()
    out["ok"] = True
    out["message"] = 'Success'
    return out    

@app.route("/users/<pid>")
def get_one_user(pid):
    out = read(int(pid))
    out["ok"] = True
    out["message"] = "Success"
    return out


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    new_id = create(
        user_data.get("first_name"),
        user_data.get("last_name"),
        user_data.get("hobbies"),
    )
    return {'ok': True, "message":"success", 'new_id':new_id}


@app.route("/users/<pid>", methods=["PUT"])
def update_user(pid):
    user_data = request.json
    out = update(int(pid), user_data)
    return {'ok': out, "message":"updated"}

@app.route("/users/<pid>", methods=["DELETE"])
def delete_user(pid):
    user_data = request.json
    out = delete(pid)
    return {'ok': out, "message":"deleted"}
