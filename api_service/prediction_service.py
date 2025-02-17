import requests


def request_prediction(property_index):
    response = requests.get(
        f'http://prediction_service:5020/predict/similar-properties?property_index={property_index}',
    )

    return response.json()