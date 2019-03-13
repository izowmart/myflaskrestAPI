from flask_restful import Resource,reqparse
from project.models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return{"message": f"A store with name {name} already exist"}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred!"}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "store deleted"}, 200
        return {"message": "An error occurred"}, 500


class StoreList(Resource):
    def get(self):
        stores = StoreModel.get_items()
        return {'store': [store.json() for store in stores]}
