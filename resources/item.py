from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint('Items', 'items', 'Operations on items')
stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

# @blp.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}
#
#
# @blp.post("/item")
# def create_item():
#     item_data = request.get_json()
#     # Here not only we need to validate data exists,
#     # But also what type of data. Price should be a float,
#     # for example.
#     if (
#             "price" not in item_data
#             or "store_id" not in item_data
#             or "name" not in item_data
#     ):
#         abort(
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#     for item in items.values():
#         if (
#                 item_data["name"] == item["name"]
#                 and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists.")
#
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#
#     return item
#
#
# @blp.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Store not found.")
#
#
# @blp.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted."}
#     except KeyError:
#         abort(404, message="Item not found.")
#
#
# @blp.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     # There's  more validation to do here!
#     # Like making sure price is a number, and also both items are optional
#     # You should also prevent keys that aren't 'price' or 'name' to be passed
#     # Difficult to do with an if statement...
#     if "price" not in item_data or "name" not in item_data:
#         abort(
#             400,
#             message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
#         )
#     try:
#         item = items[item_id]
#         item |= item_data
#
#         return item
#     except KeyError:
#         abort(404, message="Item not found.")
