from app import db
from datetime import datetime
import uuid

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    mfa_secret = db.Column(db.String(16))
    role = db.Column(db.String(20), default='provider')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    reset_token = db.Column(db.String(100))
    reset_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_in=3600):
        self.reset_token = secrets.token_urlsafe(100)
        self.reset_expiration = datetime.utcnow() + timedelta(seconds=expires_in)
        return self.reset_token

    @staticmethod
    def verify_reset_token(token):
        return User.query.filter_by(reset_token=token).first()