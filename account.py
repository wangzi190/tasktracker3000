from flask import Blueprint, render_template, request, flash, url_for, redirect
from models import User, login_manager, db

account = Blueprint('account', __name__, url_prefix='/account', template_folder='templates/account')

@account.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.form:
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirmpass=request.form['confirmpass']
        dupeUser = User.query.filter(username=username).first()
        if username and email and password:
            if password == confirmpass:
                if not dupeUser:
                    newUser = User(
                        username=username,
                        email=email,
                        password=password,
                    )
                    db.session.add(newUser)
                    db.session.commit()
                    redirect(url_for('account.login'))
                else:
                    flash('Username already taken. Please try again.')
            else:
                flash('Passwords do not match. Please try again.')
        else:
            flash('Missing required field. Please try again.')
    return render_template("/signup.html")

@account.route("/login/", methods=['GET', 'POST'])
def login():
    return render_template("/login.html")