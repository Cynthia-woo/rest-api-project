# import uuid
# from flask import Flask, request
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

# from flask_smorest import abort
# from db import stores, items


from db import db
from blocklist import BLOCKLIST
import models
import os
import secrets
# import redis

from rq import Queue


#create a functuon to create a app and inititate

def create_app(db_url=None): # allow to create an app with a certain database url, default is the local SQLite URL
    app = Flask(__name__)

    # connection = redis.from_url(
    #     os.getenv("REDIS_URL")
    # )
    # app.queue = Queue("emails", connection=connection)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)


    app.config["JWT_SECRET_KEY"] = secrets.SystemRandom().getrandbits(128)
    jwt = JWTManager(app)

    # allow user to add external information
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity): # the one comes from resourses/user.py -> login
        # look in the databse and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # create tables
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    # push context manually to app
    # with app.app_context():
    #     db.create_all()

    # @app.before_request
    # def create_tables():
    #     # The following line will remove this handler, making it
    #     # only run on the first request
    #     app.before_request_funcs[None].remove(create_tables)

    #     db.create_all()



    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app

























# @app.get("/store") # endpoint http://127.0.0.1:5000/store
# def get_stores():
#     return {"stores": list(stores.values())}

# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found.")

# @app.post("/store") # endpoint http://127.0.0.1:5000/store
# def create_stores():
#     store_data = request.get_json()
#     # check input has enough numbers
#     if "name" not in store_data:
#         abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    
#     # check if store exist
#     if stores is not None:
#         for store in stores.values():
#             if store_data["name"] == store["name"]:
#                 abort(400, messag="Store already exists.")

#     store_id = uuid.uuid4().hex #f86fa7d6f76sdsfa8df
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store
#     return store, 201

# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         return {"messsage": "Store not found."}


# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}


# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found.")


# @app.post("/item")
# def create_item():
#     # grab incoming json
#     item_data = request.get_json()
#     # 1. check the input quantity
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are inclued in the JSON payload.")

#     # check if the same
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ): 
#             abort(400, message="Item alrealy exists.")

    
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item, 201
    

# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "price" not in item_data:
#         abort(404, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

#     try:
#         item = items[item_id]
#         item |= item_data # 合并
#         # items.update(item_data)

#         return item
#     except KeyError:
#         abort(404, message="Item not found.")


# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         # items.pop(item_id)
#         return {"message": "Item deleted."}
#     except KeyError:
#         abort(404, message="Item not found.")