import requests


def save_logs(payload):
    requests.post(
        'http://logger_service:5010/logs',
        json=payload
    )