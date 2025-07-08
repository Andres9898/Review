import pytest
import json

def test_register(client):
    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data["user"]
    assert data["user"]["email"] == "test@example.com"

def test_login(client):
    # First register a user
    client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    })
    
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data

def test_invalid_login(client):
    response = client.post('/auth/login', json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_password_reset_flow(client):
    # Register a user
    client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    })
    
    # Request password reset
    response = client.post('/auth/password-reset/request', json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    
    # Get the user to get the reset token
    from app.models.user import User
    user = User.query.filter_by(email="test@example.com").first()
    assert user.reset_token is not None
    assert user.reset_expiration is not None
    
    # Confirm password reset
    response = client.post('/auth/password-reset/confirm', json={
        "token": user.reset_token,
        "password": "NewPassword123!"
    })
    
    assert response.status_code == 200
    
    # Try to log in with new password
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "NewPassword123!"
    })
    assert response.status_code == 200