#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Review object.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json
    if data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if not storage.get(User, data.get('user_id')):
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json
    if data is None:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
