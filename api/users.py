import flask
from flask import jsonify, abort
from data.db_session import create_session
from data.models.users import User
blueprint_users = flask.Blueprint("user_api", "user_api")

@blueprint_users.route("/api/users")
def users():
    return jsonify([{
        "user":{"id": i.id,
            "login":i.login,
            "email":i.email,
            "role": i.role,
            "ban": i.ban}}
                for i in create_session().query(User).all()])


@blueprint_users.route("/api/user/<int:id>")
def user(id):
    x = create_session().query(User).where(User.id == id).one()
    return jsonify({
        "user":{
            "id": x.id,
            "login":x.login,
            "email":x.email,
            "role": x.role,
            "ban": x.ban
        }
    })