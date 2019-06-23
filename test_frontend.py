from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Account
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/cashify_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# by default, direct to login
@app.route("/")
def default():
    return redirect(url_for("home"))

#Login Function     
@app.route("/home/", methods=["GET", "POST"])
def home():
    # first check if the user is already logged in
    if "username" in session:
        return render_template("userpage.html")

    # if not, and the incoming request is via POST try to log them in
    elif request.method == "POST":
        usernames = [x.username for x in User.query.all]
        thisUsername = request.form["user"]
        if thisUsername in Usernames:
            session["username"] = thisUsername

            return render_template("userpage.html")
        else:

            return render_template("homepage.html")
    else:
        # if all else fails, offer to log them in
        return render_template("homepage.html")

@app.route("/logout/")
def unlogger():
    # if logged in, log out, otherwise offer to log in
    if "username" in session:
        session.clear()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
















# CLI Commands
@app.cli.command("initdb")
def init_db():
    """Initializes database and any model objects necessary for assignment"""
    db.drop_all()
    db.create_all()

    print("Initialized Connect 4 Database.")

@app.cli.command("devinit")
def init_dev_data():
    """Initializes database with data for development and testing"""
    db.drop_all()
    db.create_all()
    print("Initialized Connect 4 Database.")


    u1 = User(username="Tyler")

    db.session.add(u1)
    db.commit()
    print("Added dummy data.")


if __name__ == "__main__":
    x = 0
    app.run(threaded=True)