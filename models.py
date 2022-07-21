from flask import Flask
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ

models = Flask(__name__, instance_relative_config=False)
models.config.update(
    SECRET_KEY=environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=environ.get('SQLALCHEMY_DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
login_manager = LoginManager()
login_manager.init_app(models)

db = SQLAlchemy()
db.init_app(models)
db.app = models

class User(UserMixin, db.Model):
    __tablename__ = 'userAccounts'
    uid = db.Column(
        db.Integer, 
        primary_key=True,
        # foreign_key=True
    )
    username = db.Column(
        db.String(256),
        unique=True,
        nullable=False,
        index=True
    )
    email = db.Column(
        db.String(256),
        unique=False,
        nullable=False,
        index=True
    )
    password = db.Column(
        db.String(256),
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

if __name__ == "__main__":
    db.create_all()