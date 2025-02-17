import requests


def is_valid_api_key(api_key):
    """ Envía la API key a subscription_manager para validación """
    response = requests.post(
        "http://subscription_manager_service:5030/subscription/auth",
        json={
            "API-Key": api_key
        }
    )
    resp = response.json()
    
    if response.status_code == 200:
        return True, resp
    
    return False, resp