from flask import request, jsonify
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app import db
from datetime import datetime, timedelta
import secrets

user_schema = UserSchema()

def register():
    try:
        data = request.get_json()
        result = user_schema.load(data)

        if User.query.filter_by(email=result['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        new_user = User(**result)
        new_user.set_password(result['password'])
        db.session.add(new_user)
        db.session.commit()

        # Send welcome email
        send_email(
            to=new_user.email,
            subject="Welcome to FarmAmigo",
            template="welcome_email",
            user=new_user
        )

        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(new_user)
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()

        if not user or not user.check_password(data.get('password')):
            return jsonify({"error": "Invalid credentials"}), 401

        if not user.is_active:
            return jsonify({"error": "Account is inactive"}), 403

        # Check if MFA is required
        if user.mfa_secret:
            token = secrets.token_hex(16)
            # Store token in session or database
            return jsonify({
                "requires_mfa": True,
                "mfa_token": token
            })

        # Generate JWT tokens
        access_token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "role": user.role
        })

        refresh_token = create_refresh_token(identity=user.id)

        user.last_login = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 500

def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            return jsonify({"error": "Invalid user"}), 401

        new_token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "role": user.role
        })

        return jsonify({"access_token": new_token}), 200

    except Exception as e:
        return jsonify({"error": "Token refresh failed", "details": str(e)}), 500

def verify_mfa():
    try:
        data = request.get_json()
        user = User.query.filter_by(id=data.get('user_id')).first()

        if not user or not user.mfa_secret:
            return jsonify({"error": "MFA not configured"}), 400

        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(data.get('code')):
            return jsonify({"error": "Invalid code"}), 400

        # Generate final tokens after MFA success
        access_token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "role": user.role
        })

        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    except Exception as e:
        return jsonify({"error": "MFA verification failed", "details": str(e)}), 500

def request_password_reset():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return jsonify({"message": "If this email exists, a reset link will be sent"}), 200

        token = user.get_reset_token()
        db.session.commit()

        reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"

        send_email(
            to=user.email,
            subject="Password Reset Request",
            template="password_reset",
            reset_link=reset_link
        )

        return jsonify({"message": "If this email exists, a reset link will be sent"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to process password reset", "details": str(e)}), 500

def confirm_password_reset():
    try:
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')

        user = User.verify_reset_token(token)

        if not user:
            return jsonify({"error": "Invalid or expired token"}), 400

        if user.check_password(password):
            return jsonify({"error": "New password cannot be the same as the old one"}), 400

        user.set_password(password)
        user.reset_token = None
        user.reset_expiration = None
        db.session.commit()

        send_email(
            to=user.email,
            subject="Your Password Has Been Changed",
            template="password_changed"
        )

        return jsonify({"message": "Password has been successfully changed"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to change password", "details": str(e)}), 500