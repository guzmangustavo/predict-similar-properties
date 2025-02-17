from flask import request, jsonify
from flask import Blueprint

from prediction import SimilarityPredictor


bp = Blueprint("predict", __name__, url_prefix="/predict")

similarity_predictor = SimilarityPredictor()


@bp.route("/similar-properties", methods=["GET"])
def similar_properties():
    property_index = int(request.args.get("property_index"))
    
    similar_properties = similarity_predictor.predict_top_n_similar_properties(
        property_index=property_index,
        top_n=10
    )
    return jsonify(similar_properties)