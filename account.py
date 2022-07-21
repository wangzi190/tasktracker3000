from flask import Blueprint, render_template, request, flash, url_for, redirect
account = Blueprint('account', __name__, url_prefix='/account', template_folder='templates/account')

@account.route("/login/")
def login():
    return render_template("/login.html")

@account.route("/signup/")
def signup():
    return render_template("/signup.html")

@account.route("/signup/", methods=['POST'])
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
                return redirect(url_for('account.login'))
            else:
                flash('Username already taken. Please try again.')
        else:
            flash('Passwords do not match. Please try again.')
    else:
        flash('Missing required field. Please try again.')
    return render_template("/signup.html")