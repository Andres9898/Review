from flask import Blueprint, request
from app.auth.controllers import (
    register, login, refresh, 
    verify_mfa, request_password_reset, 
    confirm_password_reset
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()

@auth_bp.route('/refresh', methods=['POST'])
def refresh_route():
    return refresh()

@auth_bp.route('/mfa/verify', methods=['POST'])
def verify_mfa_route():
    return verify_mfa()

@auth_bp.route('/password-reset/request', methods=['POST'])
def request_password_reset_route():
    return request_password_reset()

@auth_bp.route('/password-reset/confirm', methods=['POST'])
def confirm_password_reset_route():
    return confirm_password_reset()