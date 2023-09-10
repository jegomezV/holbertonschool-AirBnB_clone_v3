#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: amenities
-------------------------------------------------------------------------------
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Return all amenities"""
    return jsonify(list(map(lambda x: x.to_dict(),
                            storage.all(Amenity).values())))


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """Return information of a amenity"""
    try:
        return jsonify(storage.get(Amenity, amenity_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity and return a empty dictionary"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    json_amenity = request.get_json()
    if json_amenity is None:
        abort(400, "Not a JSON")
    elif "name" not in json_amenity.keys():
        abort(400, "Missing name")
    else:
        amenity = Amenity(**json_amenity)
        amenity.save()
        return (amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    new_json = request.get_json()
    if new_json is None:
        abort(400, "Not a JSON")

    for key, value in new_json.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
