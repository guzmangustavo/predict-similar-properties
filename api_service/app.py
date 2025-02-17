from flask import Flask, request, g
from routes import bp
import logger_service

import time
import uuid


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    @app.before_request
    def log_request():
        request_id = uuid.uuid4()
        request_data = {
            "request_id": str(request_id),
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
            "args": request.args.to_dict(),
            "request_body": request.get_data(as_text=True),
            "start_time": time.time()
        }
        g.request_data = request_data
    

    @app.after_request
    def after_request(response):
        if hasattr(g, 'request_data'):
            elapsed_time = time.time() - g.request_data['start_time']
            
            g.request_data.update(
                {
                    "response_time": elapsed_time,
                    "response_status_code": response.status_code,
                    "response": response.get_data(as_text=True),
                }
            )

            payload  ={
                "request_id": g.request_data["request_id"],
                "method": g.request_data["method"],
                "url": g.request_data["url"],
                "headers": g.request_data["headers"],
                "args": g.request_data["args"],
                "request_body": g.request_data["request_body"],
                "api_key": g.request_data["headers"]["X-Api-Key"],
                "response_time": g.request_data["response_time"],
                "response_status_code": g.request_data["response_status_code"],
                "response": g.request_data["response"],
            }       
                 
            logger_service.save_logs(payload=payload)
        
        return response

    return app