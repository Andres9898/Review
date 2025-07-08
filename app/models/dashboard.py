from app import db
from datetime import datetime

class DashboardMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(50), nullable=False)  # invoices_count, on_time_rate
    value = db.Column(db.Float, nullable=False)
    date_range_start = db.Column(db.DateTime, nullable=False)
    date_range_end = db.Column(db.DateTime, nullable=False)
    document_type = db.Column(db.String(20))  # invoice, delivery, etc.
    cedis_location = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)