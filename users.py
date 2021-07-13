from marshmallow import Schema, fields, post_load

def load_users():
    with open('saved_users.txt', 'r') as filehandle:
        users = list(UserSchema().dump(users, many=True))

users = []

class User(object):
    def __init__(self, name, telegram_id):
        self.name = name
        self.telegram_id = telegram_id
        self.list_id = ''


    def set_telegram_id(self, telegram_id):
        self.telegram_id = telegram_id

    def __repr__(self):
        return f'{self.name}, tg_id={self.telegram_id}'


class UserSchema(Schema):
    name = fields.String()
    telegram_id = fields.String()
    list_id = fields.String()

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


def create_user(name, telegram_id):
    users.append(User(name, telegram_id))
    save_users(users)


def show_users():
    print(len(users))
    print(users)
    return users


def save_users(users):
    with open('saved_users.json', 'w') as filehandle:
        print(UserSchema().dump(users, many=True)[0])
        filehandle.write(UserSchema().dump(users, many=True))


def load_users():
    file = open('saved_users.json', 'r')
    for f in file.read():
        print(f)
    # users = UserSchema().load(list(file.read())[0], many=True)
        # users = UserSchema().load(f)

# load_users()
