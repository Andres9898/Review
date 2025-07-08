from app import db
from datetime import datetime

class WarehouseDelivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    received_by = db.Column(db.String(36), db.ForeignKey('user.id'))
    reception_status = db.Column(db.String(20), default='pending')  # pending, received, rejected
    reception_date = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)