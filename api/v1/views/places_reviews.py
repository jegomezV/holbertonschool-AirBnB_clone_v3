#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: places_reviews
-------------------------------------------------------------------------------
"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews_from_place(place_id):
    """Return all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    list_reviews = []
    for value in place.reviews:
        list_reviews.append(value.to_dict())
    return jsonify(list_reviews)


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review(review_id):
    """Return information json of a review"""
    try:
        return jsonify(storage.get(Review, review_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review and return a empty dictionary"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new user"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json_review = request.get_json()
    if json_review is None:
        abort(400, "Not a JSON")
    elif "user_id" not in json_review.keys():
        abort(400, "Missing user_id")

    user = storage.get(User, json_review["user_id"])
    if user is None:
        abort(404)
    elif "text" not in json_review.keys():
        abort(400, "Missing text")
    else:
        json_review["place_id"] = place_id
        review = Review(**json_review)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a review by id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    new_json = request.get_json()

    if new_json is None:
        abort(400, "Not a JSON")

    for key, value in new_json.items():
        if key not in ("id", "user_id", "place_id",
                       "created_at", "updated_at"):
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
