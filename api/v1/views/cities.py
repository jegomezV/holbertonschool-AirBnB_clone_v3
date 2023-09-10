#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: states
-------------------------------------------------------------------------------
"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities_from_states(state_id):
    """Return all city from state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for value in state.cities:
        cities.append(value.to_dict())
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """Return information of a state"""
    try:
        return jsonify(storage.get(City, city_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    request_data['state_id'] = state_id
    new_city = City(**request_data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
