from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

user = Table('users', metadata,
             Column('id', Integer, primary_key=True),
             Column('first_name', String(255)),
             Column('last_name', String(255)),
             Column('age', Integer),
             Column('email', String(255)),
             )


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
