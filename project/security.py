from project.models.user import UserModel
from project import bcrypt


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
