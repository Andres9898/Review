from flask import Blueprint, request
from app.proveedores.controllers import (
    get_providers, get_provider, 
    create_provider, update_provider,
    upload_document
)

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/', methods=['GET'])
def list_providers():
    return get_providers()

@proveedores_bp.route('/<provider_id>', methods=['GET'])
def get_single_provider(provider_id):
    return get_provider(provider_id)

@proveedores_bp.route('/', methods=['POST'])
def create_new_provider():
    return create_provider()

@proveedores_bp.route('/<provider_id>', methods=['PUT'])
def update_existing_provider(provider_id):
    return update_provider(provider_id)

@proveedores_bp.route('/<provider_id>/documents', methods=['POST'])
def upload_provider_document(provider_id):
    return upload_document(provider_id)