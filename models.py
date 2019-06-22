from test_frontend import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    phone_number = db.Column(db.String(10), unique=True)
    account = relationship('Account', uselist=False, back_populates="User")


class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float(precision=2))
    user = relationship('User', back_populates='Account')


