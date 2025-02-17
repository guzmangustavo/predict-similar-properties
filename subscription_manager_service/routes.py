import secrets

from flask import Flask, request, jsonify
from flask import Blueprint

from database import insert_api_key, get_subscription_by_api_key
from service import check_request_limit


bp = Blueprint("subscription", __name__, url_prefix="/subscription")


@bp.route("/auth", methods=["POST"])
def authorize_request():
    data = request.get_json()

    api_key = data.get('API-Key', None)

    if not api_key:
        return jsonify({"error": "Falta API Key"}), 400
    
    is_allowed, message = check_request_limit(api_key)
    
    if not is_allowed:
        return jsonify({"error": message}), 429
    
    return jsonify({"message": "Solicitud autorizada"}), 200


@bp.route('/', methods=['POST'])
def create_api_key():
    data = request.get_json()

    if not data or 'type' not in data or 'limit' not in data:
        return jsonify({"error": "Faltan campos necesarios"}), 400

    api_key = secrets.token_hex(16)
    api_type = data['type']
    limit = data['limit']

    existing_api_key = get_subscription_by_api_key(api_key)
    if existing_api_key:
        return jsonify({"error": "La API Key ya existe"}), 400

    new_api_key = {
        "api_key": api_key,
        "type": api_type,
        "limit": limit
    }

    insert_result = insert_api_key(new_api_key)

    if insert_result:
        return jsonify({"api_key": api_key}), 201
    return jsonify({"message": "Error en la creación de la API Key"}), 500