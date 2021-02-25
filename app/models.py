from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, UniqueConstraint


engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

user = Table('users', metadata,
             Column('id', Integer, primary_key=True),
             Column('first_name', String(255)),
             Column('last_name', String(255)),
             Column('age', Integer),
             Column('email', String(255)),
             UniqueConstraint('email')
             )

metadata.create_all(engine)

connection = engine.connect()
