from flask import Flask, request, jsonify
from flask import Blueprint

import subscription_service
import prediction_service


bp = Blueprint("property", __name__, url_prefix="/property")


@bp.route("/<int:property_index>/similar", methods=["GET"])
def similar_properties(property_index):
    api_key = request.headers.get("x-api-key")

    if not api_key:
        return jsonify({"error": "Falta API Key en headers"}), 400
    
    if not property_index:
        return jsonify({"error": "El parámetro 'property_index' es requerido"}), 400

    is_valid_key, message = subscription_service.is_valid_api_key(api_key)

    if not is_valid_key:
        return jsonify({"error": message}), 403
    
    prediction = prediction_service.request_prediction(
        property_index=property_index
    )
    
    return jsonify(prediction)