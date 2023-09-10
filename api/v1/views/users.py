#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: users
-------------------------------------------------------------------------------
"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Return all users"""
    return jsonify(list(map(lambda x: x.to_dict(),
                            storage.all(User).values())))


@app_views.route('users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user(user_id):
    """Return information json of a user"""
    try:
        return jsonify(storage.get(User, user_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user and return a empty dictionary"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    json_user = request.get_json()
    if json_user is None:
        abort(400, "Not a JSON")
    elif "email" not in json_user.keys():
        abort(400, "Missing email")
    elif "password" not in json_user.keys():
        abort(400, "Missing password")
    else:
        user = User(**json_user)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_json = request.get_json()

    if new_json is None:
        abort(400, "Not a JSON")

    for key, value in new_json.items():
        if key not in ("id", "email", "created_at", "updated_at"):
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
