#!/usr/bin/python3
"""
Contains City api endpoints functions.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())

    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return 'Not a JSON', 400
    post_data = request.get_json()
    if 'name' not in post_data:
        return 'Missing name', 400
    new_city = City()
    for key, value in post_data.items():
        if key not in ['created_at', 'updated_at', 'id', 'state_id']:
            setattr(new_city, key, value)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        return 'Not a JSON', 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['created_at', 'updated_at', 'id', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
