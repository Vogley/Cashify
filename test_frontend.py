from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response

app = Flask(__name__)



# by default, direct to login
@app.route("/")
def default():
    return redirect(url_for("home"))

@app.route("/home/", methods=["GET", "POST"])
def home():
    return render_template("tracker.html")



if __name__ == "__main__":
    app.run(threaded=True)