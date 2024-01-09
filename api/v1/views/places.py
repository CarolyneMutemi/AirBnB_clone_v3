#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Place objects.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json
    if data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the
    JSON in the body of the request.
    """
    data = request.get_json()
    places = []
    if data is None:
        abort(400, description='Not a JSON')
    amenities = data.get('amenities')
    cities = data.get('cities')
    states = data.get('states')
    if len(data) == 0 or (not amenities and not cities and not states):
        for place in storage.all(Place):
            places.append(place.to_dict())
        return jsonify(places), 200
    if not cities and states:
        cities_list = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    cities_list.append(city)
        for city in cities_list:
            for place in city.places:
                if not amenities:
                    places.append(place.to_dict())
                else:
                    filter_amenities(place, places, amenities)
        return jsonify(places)
    if not states and cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if not amenities:
                        places.append(place.to_dict())
                    else:
                        filter_amenities(place, places, amenities)
        return jsonify(places)
    if states and cities:
        cities_list = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    cities.append(city)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in cities_list:
                cities_list.append(city)
        for city in cities_list:
            for place in city.places:
                if not amenities:
                    places.append(place.to_dict())
                else:
                    filter_amenities(place, places, amenities)
        return jsonify(places)


def filter_amenities(place_obj, places_list, amenities_list):
    """
    Applying amenity filter.
    """
    place_amenity = []
    for amenity in place_obj.amenities:
        place_amenity.append(amenity.id)
    check = all(item in place_amenity for item in amenities_list)
    if check:
        places_list.append(place_obj.to_dict())
