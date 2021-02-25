from sqlalchemy import exc
from app.schemas import UserSchema, UserExistSchema
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from http import HTTPStatus
from app.database_requests import (
    select_all,
    select_user,
    add_user,
    update_user,
    delete_user,
    select_user_by_email
)


users = Blueprint('users', __name__)
serialization_schema = UserSchema()
user_exist_schema = UserExistSchema()


@users.route('/', methods=['POST'])
def create_user():
    try:
        user_data = serialization_schema.load(request.json)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST
    try:
        add_user(user_data)
    except exc.IntegrityError:
        return f'User with "{user_data["email"]}" email already exist, please chose another one.'
    response = serialization_schema.dump(select_user_by_email(user_data['email']))
    return jsonify(response), HTTPStatus.CREATED


@users.route('/', methods=['GET'])
def read_all():
    all_users = select_all()
    response = serialization_schema.dump(all_users, many=True)
    return jsonify(response)


@users.route('/<int:user_id>', methods=['GET'])
def read_one(user_id):
    data = dict(id=user_id)
    try:
        user_exist_schema.load(data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.NOT_FOUND
    user_entity = select_user(user_id)
    return jsonify(serialization_schema.dump(user_entity))


@users.route('/<int:user_id>', methods=['PUT', 'PATCH'])
def update(user_id):
    data = dict(id=user_id, **request.json)
    try:
        user_data = user_exist_schema.load(data)
    except TypeError:
        return jsonify(message="You can't change id field"), HTTPStatus.BAD_REQUEST
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.NOT_FOUND

    try:
        update_user(user_id, user_data)
    except exc.IntegrityError:
        return f'User with "{data["email"]}" email already exist, please chose another one.'
    updated_user = select_user(user_id)

    return serialization_schema.dump(updated_user)


@users.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    data = dict(id=user_id)
    try:
        user_exist_schema.load(data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.NOT_FOUND
    delete_user(user_id)
    return '', HTTPStatus.NO_CONTENT
