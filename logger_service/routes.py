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



@bp.route('/', methods=['GET'])
def get_logs():
    try:
        logs_cursor = logs_collection.find({}, {'_id': 0})
        logs_list = list(logs_cursor)

        if not logs_list:
            return jsonify([]), 200

        return jsonify(logs_list), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500