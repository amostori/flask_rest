from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
import uuid
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import StoreModel

blp = Blueprint('Stores', 'stores', 'Operations on stores')
stores2 = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
# @blp.get("/store")
# def get_stores():
#     return {"stores": list(stores.values())}
#
#
# @blp.post("/store")
# def create_store():
#     store_data = request.get_json()
#     if "name" not in store_data:
#         abort(
#             400,
#             message="Bad request. Ensure 'name' is included in the JSON payload.",
#         )
#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             abort(400, message=f"Store already exists.")
#
#     store_id = uuid.uuid4().hex
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store
#
#     return store
#
#
# @blp.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         # Here you might also want to add the items in this store
#         # We'll do that later on in the course
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found.")
#
#
# @blp.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         abort(404, message="Store not found.")
