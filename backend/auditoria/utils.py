import json
from django.http import request as http_request


SENSITIVE_FIELDS_DENYLIST = {
    'password',
    'senha',
    'senha_hash',
    'token',
    'access',
    'refresh',
}


def get_client_ip(request):
    """Extrair IP real da requisição, considerando proxy (X-Forwarded-For)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def get_user_agent(request):
    """Extrair User-Agent da requisição."""
    return request.META.get('HTTP_USER_AGENT', '')[:255]


def remove_sensitive_fields(data):
    """Remover campos sensíveis de um dict (snapshot ou diff)."""
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if key.lower() not in SENSITIVE_FIELDS_DENYLIST:
            result[key] = value
    return result


def compute_diff(old_data, new_data):
    """
    Comparar dois dicts e retornar apenas os campos alterados.
    Formato: {campo: {de: valor_antigo, para: valor_novo}}
    """
    diff = {}
    all_keys = set(old_data.keys()) | set(new_data.keys())

    for key in all_keys:
        old_val = old_data.get(key)
        new_val = new_data.get(key)

        if old_val != new_val:
            diff[key] = {'de': old_val, 'para': new_val}

    return remove_sensitive_fields(diff)
