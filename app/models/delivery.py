from app import db
from datetime import datetime

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    actual_date = db.Column(db.DateTime)
    cedis_location = db.Column(db.String(150), nullable=False)
    carrier = db.Column(db.String(150))
    vehicle_plate = db.Column(db.String(20))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_transit, delivered, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)