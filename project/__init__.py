from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt import JWT
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.security import authenticate, identity
from project.resources.user import UserRegister
from project.resources.item import Item, ItemList
from project.resources.store import Store, StoreList

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/items')


