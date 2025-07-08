from app import db
from datetime import datetime

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, expired, paused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)