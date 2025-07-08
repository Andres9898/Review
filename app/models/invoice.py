from app import db
from datetime import datetime

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    xml_file_url = db.Column(db.String(255), nullable=False)
    pdf_file_url = db.Column(db.String(255), nullable=False)
    folio = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, validated, rejected, paid
    timbrado = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)