from datetime import datetime
from .extensions import db

class HandData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    right_hand_path = db.Column(db.String(255), nullable=False)
    left_hand_path = db.Column(db.String(255), nullable=False)