#!/usr/bin/python3
"""
Handles all default RESTFul API actions for
the link between Place objects and Amenity objects.
"""

from flask import Flask, abort, jsonify
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities_list = []
    if storage_t == 'db':
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    for amenity_id in place.amenity_ids:
        amenities_list.append(storage.get(Amenity, amenity_id).to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """
    Deletes an Amenity object to a Place.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    if amenity.id not in place.amenity_ids:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify(404), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """
    Links a Amenity object to a Place.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    if amenity.id in place.amenity_ids:
        return jsonify(amenity.to_dict()), 200
    place.amenity_ids.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
