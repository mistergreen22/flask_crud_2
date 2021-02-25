from app.models import user, connection


def select_user(user_id):
    select_user_action = user.select().where(user.columns.id == user_id)
    selected_user = connection.execute(select_user_action).fetchone()
    return selected_user


def select_user_by_email(user_email):
    select_user_action = user.select().where(user.columns.email == user_email)
    selected_user = connection.execute(select_user_action).fetchone()
    return selected_user


def select_all():
    select_users = user.select()
    users = connection.execute(select_users).fetchall()
    return users


def add_user(user_data):
    ins = user.insert().values(user_data)
    connection.execute(ins)


def update_user(user_id, user_data):
    update_user_action = user.update().where(
        user.columns.id == user_id
    ).values(user_data)
    connection.execute(update_user_action)


def delete_user(user_id):
    used_delete_action = user.delete().where(user.columns.id == user_id)
    connection.execute(used_delete_action)
