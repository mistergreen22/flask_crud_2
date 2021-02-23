from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from marshmallow import Schema, fields, ValidationError, post_load


engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

user = Table('users', metadata,
             Column('id', Integer, primary_key=True),
             Column('first_name', String(255)),
             Column('last_name', String(255)),
             Column('age', Integer),
             Column('email', String(255)),
             )


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    email = fields.Email()


class UserExistSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    email = fields.Email()

    @post_load
    def check_existence(self, data, **kwargs):
        select_action = user.select().where(user.columns.id == data['id'])
        selected_user = connection.execute(select_action).fetchone()
        if selected_user is None:
            raise ValidationError(message="User doesn't exist")
        return data


# deprecated
def to_json(data):
    return {
        "id": data[0],
        "first_name": data[1],
        "last_name": data[2],
        "age": data[3],
        "email": data[4]
    }


metadata.create_all(engine)

connection = engine.connect()
