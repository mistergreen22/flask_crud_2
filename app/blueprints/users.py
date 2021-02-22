from flask import Blueprint, request, jsonify
from app.models import user, connection, UserSchema, UpdateSchema
from marshmallow import ValidationError
from http import HTTPStatus


users = Blueprint('users', __name__)
serial_schema = UserSchema()
update_schema = UpdateSchema()


@users.route('/', methods=['POST'])
def create_user():
    try:
        response = serial_schema.load(request.json)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST
    ins = user.insert().values(response)
    connection.execute(ins)
    return response, HTTPStatus.CREATED


@users.route('/', methods=['GET'])
def read_all():
    s_all = user.select()
    o = connection.execute(s_all).fetchall()
    response = serial_schema.dump((o), many=True)
    return jsonify(response)


@users.route('/<int:user_id>', methods=['GET'])
def read_one(user_id):
    s = user.select().where(user.columns.id == user_id)
    o = connection.execute(s).fetchone()
    if o is None:
        return '', HTTPStatus.NOT_FOUND
    return jsonify(serial_schema.dump(o))


@users.route('/<int:user_id>', methods=['PUT', 'PATCH'])
def update(user_id):

    try:
        data = dict(id=user_id, **request.json)
        response = update_schema.load(data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.BAD_REQUEST

    u = user.update().where(
        user.columns.id == user_id
    ).values(response)
    connection.execute(u)

    s = user.select().where(user.columns.id == user_id)
    c = connection.execute(s).fetchone()

    return serial_schema.dump(c)


@users.route('/<user_id>', methods=['DELETE'])
def delete(user_id):
    try:
        r = serial_schema.load(request.json)
    except ValidationError as err:
        pass
    u = user.delete().where(user.columns.id == user_id)
    o = connection.execute(u)
    if o.rowcount == 0:
        return '', HTTPStatus.NOT_FOUND
    return '', HTTPStatus.NO_CONTENT
