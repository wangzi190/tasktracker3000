from flask import Flask
from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(
    __name__,
    # template_folder="templates"
)

# Development configuration
app.config.from_object('config.DevConfig')

# Production configuration
# app.config.from_object('config.ProdConfig')

from flask_login import LoginManager
login_manager = LoginManager()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")