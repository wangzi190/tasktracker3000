from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
from os import environ

main = Flask(__name__, template_folder='templates')
main.config.update(
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development',
    SQLALCHEMY_DATABASE_URI='sqlite:///students.sqlite3'
)

login_manager = LoginManager()
loginApp = Flask(__name__)
login_manager.init_app(loginApp)
loginApp.config.update(
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development',
    SQLALCHEMY_DATABASE_URI='sqlite:///students.sqlite3'
)
loginApp.secret_key = environ.get('SECRET_KEY')

@main.route("/")
def index():
    return render_template("/index.html")

@main.route("/about/")
def about():
    return render_template("/about.html")

@main.route("/account/")
def account():
    return render_template("/logreg.html")

""" @main.route('account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        loginbool = request.form[loginbool]
        signupbool = request.form[signupbool]
        if loginbool != 0:
            lusername = request.form[lusername]
            lpassword = request.form[lpassword]
            lremember = request.form[lremember]
        if signupbool != 0:
            susername = request.form[susername]
            semail = request.form[semail]
            spassword = request.form[spassword]
            sconfirmpass = request.form[sconfirmpass]
    return render_template("/logreg.html")
    # return redirect(url_for('index')) """ 

if __name__ == "__main__":
  main.run(debug=True)