from flask import Blueprint, request, jsonify
from app.models import user, connection, to_json
from sqlalchemy import text

users = Blueprint('users', __name__)


@users.route('/', methods=['POST'])
def create_user():
    ins = user.insert().values(first_name=request.json['first_name'],
                               last_name=request.json['last_name'],
                               age=request.json['age'],
                               email=request.json['email'])
    connection.execute(ins)
    return jsonify(ins.parameters), 201


@users.route('/', methods=['GET'])
def read_all():
    s_all = user.select()
    o = connection.execute(s_all).fetchall()
    return jsonify([to_json(d) for d in o])


@users.route('/<user_id>', methods=['GET'])
def read_one(user_id):
    s = user.select().where(user.columns.id == user_id)
    o = connection.execute(s).fetchone()
    if o is None:
        return '', 404
    return jsonify(to_json(o))
