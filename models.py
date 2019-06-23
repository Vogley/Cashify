from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    phone_number = db.Column(db.String(10), unique=True)
    account = db.relationship("Account", backref="user_name", lazy="select")


class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float(precision=2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
