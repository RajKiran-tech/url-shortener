from flask import Blueprint, request, jsonify
from app.services import user_service

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(user_service.get_all_users())

@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return user_service.get_user_by_id(user_id)

@user_bp.route("/users", methods=["POST"])
def create_user():
    return user_service.create_user(request.json)

@user_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    return user_service.update_user(user_id, request.json)

@user_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    return user_service.delete_user(user_id)

@user_bp.route("/search", methods=["GET"])
def search_user():
    name = request.args.get("name")
    return jsonify(user_service.search_users_by_name(name))

@user_bp.route("/login", methods=["POST"])
def login():
    return user_service.authenticate_user(request.json)
