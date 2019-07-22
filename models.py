from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship("Account", foreign_keys=[account_id], backref="user_id")


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactions = db.relationship("Transaction", backref="account")
    balance = db.Column(db.Float(precision=2))
    categories = db.relationship("Category", backref="account_number", lazy="select") # Not sure if the lazy param is needed

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=2))
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20))
    current_balance = db.Column(db.Float(precision=2))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
