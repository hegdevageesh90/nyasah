from flask import Blueprint, request, jsonify
from app.services.user_generated_content_service import add_user_generated_content, get_content_by_user, \
    get_content_by_type, update_ugc, get_content_by_content_id

from app.models.user_generated_content import UserGeneratedContent

ugc_bp = Blueprint('ugc_bp', __name__)


@ugc_bp.route('/ugc', methods=['POST'])
def create_user_generated_content():
    content_data = request.json
    try:
        content = UserGeneratedContent(**content_data)
        saved_content = add_user_generated_content(content)
        return jsonify(saved_content), 201
    except Exception as e:
        return str(e), 400


@ugc_bp.route('/ugc/<content_id>', methods=['PUT'])
def update_ugc_route(content_id):
    data = request.get_json()
    result = update_ugc(content_id, data)
    return jsonify(result), 200

@ugc_bp.route('/ugc/<string:content_id>', methods=['GET'])
def get_content_by_content_id_route(content_id):
    content_list = get_content_by_content_id(content_id)
    return jsonify(content_list), 200


@ugc_bp.route('/ugc/user/<string:user_id>', methods=['GET'])
def get_content_by_user_route(user_id):
    content_list = get_content_by_user(user_id)
    return jsonify(content_list), 200


@ugc_bp.route('/ugc/type/<string:content_type>', methods=['GET'])
def get_content_by_type_route(content_type):
    content_list = get_content_by_type(content_type)
    return jsonify(content_list), 200
