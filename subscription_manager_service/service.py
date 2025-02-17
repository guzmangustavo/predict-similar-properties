import time 
from database import redis_client, get_subscription_by_api_key


def check_request_limit(api_key):
    subscription = get_subscription_by_api_key(api_key)
    if not subscription:
        return False, "API Key no válida o no registrada"
    
    limit = subscription["limit"]
    
    key = f"rate_limit:{api_key}"
    current_time = int(time.time())
    window_start = current_time - (current_time % 60)
    
    requests_made = redis_client.get(f"{key}:{window_start}") or 0
    requests_made = int(requests_made)
    
    if requests_made < limit:
        redis_client.incr(f"{key}:{window_start}")
        return True, "Solicitud autorizada"
    else:
        return False, f"Límite de {limit} solicitudes por minuto alcanzado"