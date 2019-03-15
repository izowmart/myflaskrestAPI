from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from project.blacklist import BLACKLIST

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.resources.user import UserRegister, User, UserLogout, UserLogin, UserList, TokenRefresh
from project.resources.item import Item, ItemList
from project.resources.store import Store, StoreList

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has expired.",
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed.",
        "error": "Invalid_token"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        "error": "token_revoked"
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


