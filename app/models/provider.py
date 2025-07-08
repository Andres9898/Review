from app import db
from datetime import datetime
import json

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(150), nullable=False)
    legal_name = db.Column(db.String(150))
    rfc = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(50))
    documents = db.Column(db.Text)  # JSON array of document metadata
    status = db.Column(db.String(20), default='pending')  # pending, approved, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def add_document(self, doc_data):
        docs = json.loads(self.documents) if self.documents else []
        docs.append(doc_data)
        self.documents = json.dumps(docs)