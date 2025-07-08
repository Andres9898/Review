from app import db
from datetime import datetime

class Evidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, jpeg, png
    uploaded_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)