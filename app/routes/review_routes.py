from flask import Blueprint, request, jsonify

from app.models.review import Review
from app.services.review_service import add_review, get_reviews_by_product

review_bp = Blueprint('review_bp', __name__)


@review_bp.route('/reviews', methods=['POST'])
def create_review():
    # Parse the incoming JSON body into the Review model
    review_data = request.json

    # Convert dict to Review model instance
    review = Review(**review_data)

    # Call service function to add the review
    saved_review = add_review(review)

    return jsonify(saved_review), 201


@review_bp.route('/reviews/<product_id>', methods=['GET'])
def list_reviews(product_id):
    reviews = get_reviews_by_product(product_id)
    return jsonify(reviews), 200
