from app import db
from datetime import datetime

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_type = db.Column(db.String(20), nullable=False)  # shortage, damage, out_of_spec
    reported_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)