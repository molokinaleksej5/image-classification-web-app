from datetime import datetime
from core.database import db


class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    predicted_class = db.Column(db.String(120), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    probabilities_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)