from flask import Flask, render_template
from account import account

main = Flask(__name__, template_folder='templates')
main.register_blueprint(account)
main.config.update(
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development',
)

@main.route("/")
def index():
    return render_template("/index.html")

@main.route("/about/")
def about():
    return render_template("/about.html")

@main.route("/tasks/")
def tasks():
    return render_template("/tasks.html")

if __name__ == "__main__":
  main.run(debug=True)