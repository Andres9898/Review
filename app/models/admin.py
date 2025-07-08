from app import db
from datetime import datetime

class AdminUser(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='admin')
    assigned_by = db.Column(db.String(36), db.ForeignKey('user.id'))  # Quién lo asignó
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(20), nullable=False)  # csv, pdf
    generated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    filters = db.Column(db.Text)  # JSON con filtros usados
    file_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)