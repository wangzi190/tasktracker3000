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
from tasks import tasks
main.register_blueprint(tasks)
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
    id = db.Column(
        db.Integer, 
        primary_key=True,
        nullable=False,
    )
    username = db.Column(
        db.String(256),
        unique=True,
        nullable=False,
    )
    email = db.Column(
        db.String(256),
        nullable=False,
    )
    password = db.Column(
        db.String(256),
        nullable=False
    )
    tasks = db.relationship(
        "Task",
        backref='user'
    )
    categories = db.relationship(
        "Category",
        backref='user'
    )
    stickers = db.relationship(
        "Sticker",
        backref='user'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def get_id(self):
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

class Task(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    month = db.Column(
        db.Integer,
        nullable=False,
    )
    day = db.Column(
        db.Integer,
        nullable=False
    )
    year = db.Column(
        db.Integer,
        nullable=False,
    )
    taskName = db.Column(
        db.String(256),
        nullable=False
    )
    category = db.Column(
        db.Integer,
        nullable=False
    )
    progress = db.Column(
        db.Integer,
        nullable=False,
    )
    sections = db.Column(
        db.Integer,
        nullable=False
    )
    value = db.Column(
        db.Integer,
        nullable=False
    )
    completed = db.Column(
        db.Boolean,
        nullable=False
    )
    stickers = db.Column(
        db.String(256),
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.taskName)

    def __init__(self, user_id, month, day, year, taskName, category, progress, sections, value, completed, stickers):
        self.user_id = user_id
        self.month = month
        self.day = day
        self.year = year
        self.taskName = taskName
        self.category = category
        self.progress = progress
        self.sections = sections
        self.value = value
        self.completed = completed
        self.stickers = stickers

    def get_id(self):
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

class Category(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    categoryName = db.Column(
        db.String(256),
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.taskName)

    def __init__(self, user_id, categoryName):
        self.user_id = user_id
        self.categoryName = categoryName

    def get_id(self):
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

class Sticker(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    stickerFile = db.Column(
        db.String(256),
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.taskName)

    def __init__(self, user_id, stickerFile):
        self.user_id = user_id
        self.stickerFile = stickerFile

    def get_id(self):
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

if __name__ == "__main__":
    main.run(debug=True)
    # db.create_all()