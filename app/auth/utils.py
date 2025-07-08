from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return jsonify(msg="Admin access required"), 403
        return fn(*args, **kwargs)
    return wrapper

def provider_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if current_user.get('role') != 'provider':
            return jsonify(msg="Provider access required"), 403
        return fn(*args, **kwargs)
    return wrapper

def warehouse_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if current_user.get('role') != 'warehouse':
            return jsonify(msg="Warehouse access required"), 403
        return fn(*args, **kwargs)
    return wrapper

def logistics_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if current_user.get('role') not in ['logistics', 'admin']:
            return jsonify(msg="Logistics access required"), 403
        return fn(*args, **kwargs)
    return wrapper