import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores
from db import db
from schemas import StoreSchema
from models import StoreModel

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# blueprint: used to devide apis in several segments


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(400, message="Store not found.")
        store = StoreModel.query.get_or_404(store_id)
        return store # within the store schema: so it will be turned into json

    def delete(self, store_id):
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     return {"messsage": "Store not found."}
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}
        
@blp.route("/store")
class Store(MethodView):
    @blp.response(200, StoreSchema(many = True))
    def get(self):
        # return {"stores": list(stores.values())}
        # return stores.values()
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self,store_data):
        # store_data = request.get_json()
        # # check input has enough numbers
        # if "name" not in store_data:
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        
        # check if store exist
        # if stores is not None:
        #     for store in stores.values():
        #         if store_data["name"] == store["name"]:
        #             abort(400, messag="Store already exists.")

        # store_id = uuid.uuid4().hex #f86fa7d6f76sdsfa8df
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store

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