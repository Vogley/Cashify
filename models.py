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
    categories = db.relationship("Category", backref="account_name", lazy="select") # Not sure if the lazy param is needed
    budget = db.relationship("Budget", backref="account_name", lazy="select", uselist=False)

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

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    total_budget = db.Column(db.Float)
    income = db.Column(db.Float)
    rent = db.Column(db.Float)
    education = db.Column(db.Float)
    groceries = db.Column(db.Float)
    home_improvement = db.Column(db.Float)
    entertainment = db.Column(db.Float)
    savings = db.Column(db.Float)
    utilities = db.Column(db.Float)
    auto_gas = db.Column(db.Float)
    healthcare = db.Column(db.Float)
    restaurants = db.Column(db.Float)
    shopping = db.Column(db.Float)
    travel = db.Column(db.Float)
    other = db.Column(db.Float)