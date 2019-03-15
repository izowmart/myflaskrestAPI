from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from flask_restful import reqparse, Resource
from project.models.user import UserModel
from project.blacklist import BLACKLIST
from project import bcrypt

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='This field cannot be left empty'
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cannot be left empty'
                          )


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    @jwt_required
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        users = UserModel.get_all()
        if users:
            return {"users": [user.json() for user in users]}
        return {"message": "No user found"}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is  "JWT ID" a unique identifier for jwt
        BLACKLIST.add(jti)
        return {"messaage": "Successfully logged out."}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # here we already have a refresh token
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
