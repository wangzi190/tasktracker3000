from flask import Flask
from flask import Flask, render_template, request
from pathlib import Path
main = Flask(__name__, template_folder='templates')

from logging import FileHandler,WARNING
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

main.config.update(
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development'
)

@main.route("/")
def index():
    return render_template("/index.html")

@main.route("/about/")
def about():
    return render_template("/about.html")

if __name__ == "__main__":
  main.run(debug=True)

# py -u "c:\Users\Owner\myprojects\tasktracker3000\main.py"