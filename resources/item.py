import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
# from db import items
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

from db import db
from sqlalchemy.exc import SQLAlchemyError


# blueprint: used to devide apis in several segments


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id) # will automatically aboard to 404 if is not this
            return item
            # return items[item_id]
        except KeyError:
            abort(400, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()
        
        # if "price" not in item_data or "price" not in item_data:
        #     abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

        # try:
        #     # item = items[item_id]
        #     item = db.session.get(item_id)
        #     item |= item_data # 合并
        #     # items.update(item_data)

        #     return item
        # except KeyError:
        #     abort(400, message="Item not found.")

        item = ItemModel.query.get(item_id)
        if item: # if item exists, update
            item.price = item_data["price"]
            item.name = item_data["name"]
        else: # if not, create a new one
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

            

    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

        # try:
        #     # del items[item_id]
        #     item = db.session.get(item_id)
        #     db.session.remove(item)
        #     # items.pop(item_id)
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     abort(400, message="Item not found.")


@blp.route("/item")
class Item(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
    #     # return {"items": list(items.values())}
    #     return items.values()
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # # grab incoming json
        # item_data = request.get_json()

        ##---- replaced with schema ----##
        # # 1. check the input quantity
        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are inclued in the JSON payload.")

        # check if the same
        # for item in items.values():
        #     if (
        #         item_data["name"] == item["name"]
        #         and item_data["store_id"] == item["store_id"]
        #     ): 
        #         abort(400, message="Item alrealy exists.")
        
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item

        item = ItemModel(**item_data) # turn it to keyword arguments, and then pass them into the model
        # then try to insert into the database
        
        try:
            db.session.add(item) # add
            db.session.commit() # saving to the disc
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return item