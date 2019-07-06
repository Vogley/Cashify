from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    phone_number = db.Column(db.String(10), unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship("Account", foreign_keys=[account_id], backref="user_account")


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactions = db.relationship("Transaction", backref="account_name", lazy="select")
    balance = db.Column(db.Float(precision=2))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=2))
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20))
    current_balance = db.Column(db.Float(precision=2))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))