from marshmallow import Schema, fields, post_load

users = []

class User(object):
    def __init__(self, name, telegram_id):
        self.name = name
        self.telegram_id = telegram_id
        self.list_id = ''

    
    def set_telegram_id(self, telegram_id):
        self.telegram_id = telegram_id
    
    def __repr__(self):
        return f'{self.name}'


class UserSchema(Schema):
    name = fields.String()
    telegram_id = fields.String()
    list_id = fields.String()


def create_user(name, telegram_id):
    users.append(User(name, telegram_id))

    
def show_users():
    print(len(users))
    print(users)
    return users