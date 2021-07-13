from marshmallow import Schema, fields, post_load
import pickle

def load_users():
    with open('saved_users.txt', 'r') as filehandle:
        users = list(UserSchema().dump(users, many=True))

users = []

class User(object):
    def __init__(self, name, telegram_id, list_id=''):
        self.name = name
        self.telegram_id = telegram_id
        self.list_id = list_id


    def set_telegram_id(self, telegram_id):
        self.telegram_id = telegram_id

    def __repr__(self):
        return f'{self.name} - tg_id={self.telegram_id}'


class UserSchema(Schema):
    name = fields.String()
    telegram_id = fields.Integer()
    list_id = fields.String()

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


def create_user(name, telegram_id):
    users.append(User(name, telegram_id))
    save_users()


def show_users():
    return users


def save_users():
    data = UserSchema().dump(users, many=True)
    with open("saved_users.txt", "wb") as saved_users:
        pickle.dump(data, saved_users)


def load_users():
    with open("saved_users.txt", "rb") as saved_users:
        data = pickle.load(saved_users)
    global users
    users = UserSchema().load(data, many=True)

def get_all_users():
    return(users)

load_users()