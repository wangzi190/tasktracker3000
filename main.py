from flask import Flask, render_template
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

main = Flask(__name__, template_folder='templates')
from account import account
main.register_blueprint(account)
main.config.update(
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development',
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

login_manager = LoginManager()
login_manager.init_app(main)
login_manager.login_view = 'account.login'

db = SQLAlchemy(main)
db.init_app(main)

@main.route("/")
def index():
    return render_template("/index.html")

@main.route("/about")
def about():
    return render_template("/about.html")

@main.route("/tasks")
def tasks():
    return render_template("/tasks.html")

class User(UserMixin, db.Model):
    uid = db.Column(
        db.Integer, 
        primary_key=True,
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

    def get_id(self):
        return self.uid

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

if __name__ == "__main__":
    main.run(debug=True)