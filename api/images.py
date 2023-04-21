import flask
from flask import jsonify, abort

blueprint_images = flask.Blueprint("image_api", "image_api")


@blueprint_images.route("/images/<string:img>")
def a(img):
    return jsonify({"ss": "ss"})