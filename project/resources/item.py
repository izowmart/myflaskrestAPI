from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from project.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}, 200
        return {"message": f"Item by the name {name} does not exist"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # create a new item
            item = ItemModel(name, **data)
            item.save_to_db()
        else:
            # update the existing one
            item.price = data['price']
            item.save_to_db()
            return {"message": "Item updated successfully"}, 200
        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.get_items()
        return {'items': list(map(lambda x: x.json(), items))}, 200
