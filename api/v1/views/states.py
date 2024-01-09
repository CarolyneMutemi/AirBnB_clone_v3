#!/usr/bin/python3
"""
Handles all default RESTFul API actions for State objects.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects
    """
    list_states = []
    for state in storage.all(State).values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.
    """
    if not storage.get(State, state_id):
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State.
    """
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if "name" not in data:
        abort(400, 'Missing name')
    new_obj = State(name=data.get("name"))
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
