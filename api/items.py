import flask
from flask import jsonify, abort
from data.db_session import create_session
from data.models.item import Item
blueprint_items = flask.Blueprint("item_api", "item_api")

@blueprint_items.route("/api/items")
def items():
    return jsonify([{
        "items":{
            "id": i.id,
            "price":i.price,
            "about":i.about,
            "title": i.title}}
               for i in create_session().query(Item).all()])


@blueprint_items.route("/api/item/<int:id>")
def item(id):
    i = create_session().query(Item).where(Item.id == id).one()
    return jsonify({
        "item": {"id": i.id,
              "price": i.price,
              "about": i.about,
              "title": i.title}})


