from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
account = Blueprint('account', __name__, url_prefix='/account', template_folder='templates/account')

@account.route("/login")
def login():
    return render_template("/login.html")

@account.route("/login", methods=['POST'])
def login_action():
    from main import User
    username=request.form['username']
    password=request.form['password']
    if request.form['remember'] == None:
        remember=False
    else:
        remember=True
    validName = User.query.filter_by(username=str(username)).first()
    validPass = check_password_hash(validName.password, password)
    if validName:
        if validPass:
            identifier = User.query.filter_by(uid=validName.uid).first()
            password=generate_password_hash(password, method='sha256')
            returningUser = User(
                str(username),
                identifier.email,
                str(password)
            )
            login_user(returningUser, remember=remember)
            flash('Successfully logged in.')
            return redirect(url_for('index'))
        else:
            flash('Invalid password. Please try again.')
    else:
        flash('Invalid username. Please try again.')
    return render_template("/login.html")

@account.route("/logout")
@login_required
def logout():
    flash('Successfully logged out.')
    return redirect(url_for('index'))

@account.route("/signup")
def signup():
    return render_template("/signup.html")

@account.route("/signup", methods=['POST'])
def signup_action():
    from main import User, db
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    confirmpass=request.form['confirmpass']
    dupeUser = User.query.filter_by(username=str(username)).first()
    if username and email and password:
        if password == confirmpass:
            if not dupeUser:
                newUser = User(
                    str(username),
                    str(email),
                    str(password),
                )
                db.session.add(newUser)
                db.session.commit()
                flash('Account successfully created. Please log in.')
                return redirect(url_for('account.login'))
            else:
                flash('Username already taken. Please try again.')
        else:
            flash('Passwords do not match. Please try again.')
    else:
        flash('Missing required field. Please try again.')
    return render_template("/signup.html")