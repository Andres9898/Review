from app import db
from datetime import datetime

class CreditNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, issued, applied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)