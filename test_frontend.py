from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/cashify_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# by default, direct to login
@app.route("/")
def default():
    return redirect(url_for("home"))

@app.route("/home/", methods=["GET", "POST"])
def home():
    return render_template("tracker.html")



if __name__ == "__main__":
    app.run(threaded=True)