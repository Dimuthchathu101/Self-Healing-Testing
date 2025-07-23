from .db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'deposit' or 'withdrawal' or 'transfer'
    timestamp = db.Column(db.DateTime, nullable=False)

class Locator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(80), nullable=False)
    element_name = db.Column(db.String(80), nullable=False)
    selector_type = db.Column(db.String(20), nullable=False)  # e.g., 'id', 'css', 'xpath'
    selector_value = db.Column(db.String(200), nullable=False) 