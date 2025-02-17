import datetime

from bson import ObjectId
from flask import Flask, request, jsonify
from flask import Blueprint
from database import logs_collection


bp = Blueprint("logs", __name__, url_prefix="/logs")


@bp.route('/', methods=['POST'])
def register_log():
    try:
        data = request.get_json()
        
        log_entry = {
            "request_id": data['request_id'],
            "method": data['method'],
            "url": data['url'],
            "headers": data['headers'],
            "args": data['args'],
            "request_body": data['request_body'],
            "api_key": data['api_key'],
            "response_time": data['response_time'],
            "response_status_code": data['response_status_code'],
            "response": data['response'],
            "timestamp": datetime.datetime.now()
        }
        
        result = logs_collection.insert_one(log_entry)
        
        if result.inserted_id:
            return jsonify({
                "status": "logged",
                "log_id": str(result.inserted_id)
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to insert log"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@bp.route('/<log_id>', methods=['GET'])
def get_log(log_id):
    try:
        if not ObjectId.is_valid(log_id):
            return jsonify({
                "status": "error",
                "message": "Invalid log ID format"
            }), 400

        log = logs_collection.find_one(
            {"_id": ObjectId(log_id)},
            {'_id': 0}
        )

        if not log:
            return jsonify({
                "status": "error",
                "message": "Log not found"
            }), 404

        return jsonify({"log": log}), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500