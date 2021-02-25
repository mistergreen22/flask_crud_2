from marshmallow import Schema, fields, ValidationError, post_load
from models import user, connection


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    email = fields.Email(required=True)


class UserExistSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    email = fields.Email(required=True)

    @post_load
    def check_existence(self, data, **kwargs):
        select_action = user.select().where(user.columns.id == data['id'])
        selected_user = connection.execute(select_action).fetchone()
        if selected_user is None:
            raise ValidationError(message="User doesn't exist")
        return data
