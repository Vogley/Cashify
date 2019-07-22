from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Account, Transaction, Category, Budget
from datetime import datetime
import os
import re

app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/cashify_dev"

# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


'''*****RESTful Resources*****'''
parser = reqparse.RequestParser()
parser.add_argument('Amount')
parser.add_argument('Category')

parser.add_argument('Total Budget')
parser.add_argument('Income')
parser.add_argument('Rent')
parser.add_argument('Education')
parser.add_argument('Groceries')
parser.add_argument('Home Improvement')
parser.add_argument('Entertainment')
parser.add_argument('Savings')
parser.add_argument('Utilities')
parser.add_argument('Auto')
parser.add_argument('Healthcare')
parser.add_argument('Restaurants')
parser.add_argument('Shopping')
parser.add_argument('Travel')
parser.add_argument('Other')



# Game Resource
# Creates Games and Deletes Games
class MyTransaction(Resource):
    def delete(self, transaction_id):
        Transaction.query.filter_by(id=transaction_id).delete()
        db.session.commit()
        return '', 204


# TransactionList
# shows a list of all transactions, and lets you POST to add new transactions
class TransactionList(Resource):
    def get(self):
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        transactions = account.transactions

        if(len(transactions) != 0):
            transactionList = []
            #transactionList will include the information of each transaction. Amount, date, and category. The last object is the user's account at that moment.
            for t in transactions:
                transactionList.append(t.date)
                transactionList.append(t.amount)
                transactionList.append(t.category)
                transactionList.append(t.current_balance)
            return transactionList
        else:
            return None

    def post(self):
        args = parser.parse_args() 
        amount = args['Amount']      
        category = args['Category']

        # Get the user
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        transactions = account.transactions
        tempBalance = account.balance + float(amount)
        account.balance = round(tempBalance, 2)
        balance = account.balance 


        dateX = datetime.now()
        date = myconverter(dateX)

        # Create the Transaction
        t = Transaction(amount=amount, date=date, category=category, current_balance=balance)
        db.session.add(t)
        account.transactions.append(t)
        db.session.commit()

        return t.id, 201


# List
# shows a list of all transactions, and lets you POST to add new transactions
class UserBudget(Resource):
    def get(self):
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        budget = account.budget

        if budget:
            budgetList = []
            #budgetList will include the information of the user budget. Amount, date, and category. The last object is the user's account at that moment.
            budgetList.append(budget.total_budget)
            budgetList.append(budget.income)
            budgetList.append(budget.rent)
            budgetList.append(budget.education)
            budgetList.append(budget.groceries)
            budgetList.append(budget.home_improvement)
            budgetList.append(budget.entertainment)
            budgetList.append(budget.savings)
            budgetList.append(budget.utilities)
            budgetList.append(budget.auto_gas)
            budgetList.append(budget.healthcare)
            budgetList.append(budget.restaurants)
            budgetList.append(budget.shopping)
            budgetList.append(budget.travel)
            budgetList.append(budget.other)
            return budgetList
        else:
            return None

    def put(self):
        args = parser.parse_args()
        total_budget = args['Total Budget']
        income = args['Income']
        rent = args['Rent']
        education = args['Education']
        groceries = args['Groceries']
        home_improvement = args['Home Improvement']
        entertainment = args['Entertainment']
        savings = args['Savings']
        utilities = args['Utilities']
        auto_gas = args['Auto']
        healthcare = args['Healthcare']
        restaurants = args['Restaurants']
        shopping = args['Shopping']
        travel = args['Travel']
        other = args['Other']

        # Get the user
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account

        # Create the Budget
        b = Budget(account_id=account.id, total_budget=total_budget, income=income, rent=rent, education=education, groceries=groceries, home_improvement=home_improvement,
                   entertainment=entertainment, savings=savings, utilities=utilities, auto_gas=auto_gas, healthcare=healthcare, restaurants=restaurants,
                   shopping=shopping, travel=travel, other=other)

        record = db.session.query(Budget).filter(Budget.account_id == account.id).first()

        if record is None:
            db.session.add(b)
            account.budget = b

        else:
            record.total_budget = total_budget
            record.income = income
            record.rent = rent
            record.education = education
            record.groceries = groceries
            record.home_improvement = home_improvement
            record.entertainment = entertainment
            record.savings = savings
            record.utilities = utilities
            record.auto_gas = auto_gas
            record.healthcare = healthcare
            record.restaurants = restaurants
            record.shopping = shopping
            record.travel = travel
            record.other = other

        db.session.commit()

        return b.id, 201



def myconverter(o):
    if isinstance(o, datetime):
        #Formatting
        if(o.month < 10):
            month = "0" + str(o.month)
        else:
            month = o.month
        if(o.day < 10):
            day = "0" + str(o.day)
        else:
            day = o.day

        return "{}-{}-{}".format(o.year, month, day)



##
## Actually setup the Api resource routing here
##
api.add_resource(TransactionList, '/transactions')
api.add_resource(MyTransaction, '/transactions/<transaction_id>')
api.add_resource(UserBudget, '/budget')


'''*****Webpage Functions*****'''
# by default, direct to login
@app.route("/")
def default():
    return redirect(url_for("home"))


# Login Function
@app.route("/home/", methods=["GET", "POST"])
def home():
    # first check if the user is already logged in
    if "username" in session:
        user = User.query.get(1)
        for u in User.query.all():
            if u.username == session["username"]:
                user = u

        return render_template("userpage.html", user=user)

    # if not, and the incoming request is via POST try to log them in
    elif request.method == "POST":
        usernames = [x.username for x in User.query.all()]
        thisUsername = request.form["username"]
        thisPassword = request.form["password"]
        if thisUsername in usernames:
            user = User.query.get(1)
            for u in User.query.all():
                if u.username == thisUsername:
                    user = u

            if thisPassword == user.password_hash:
                session["username"] = thisUsername
                return render_template("userpage.html", user=user)
            else:
                return render_template("homepage.html")
        else:
            return render_template("homepage.html")
    else:
        return render_template("homepage.html")


@app.route("/logout/")
def unlogger():
    # if logged in, log out, otherwise offer to log in
    if "username" in session:
        session.clear()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


# Redirects user to registration page with their information.
@app.route("/registration/", methods=["POST"])
def regRedirect():
    rUsername = request.form["rusername"]
    rPassword = request.form["rpassword"]
    cPassword = request.form["cpassword"]   
    if rUsername != "" and rPassword != "" and cPassword != "":
        return render_template("registration.html", rusername=rUsername, rpassword=rPassword, cpassword=cPassword)
    else:
        return redirect(url_for("home"))


@app.route("/registrationCheck/", methods=["POST"])
def registration():
    usernames = [x.username for x in User.query.all()]
    emails = [y.email for y in User.query.all()]
    rFirstName = request.form["rfirstname"]
    rLastName = request.form["rlastname"]
    email = request.form["email"]
    amount = request.form["amount"]
    rUsername = request.form["rusername"]
    rPassword = request.form["rpassword"]
    cPassword = request.form["cpassword"]
    if rUsername in usernames or email in emails:
        # username and email should be blank because one of them is already being used
        return render_template("registration.html", rpassword=rPassword, cpassword=cPassword, rfirstname=rFirstName, rlastname=rLastName, amount=amount) 
        '''TODO: I want to be able to return to the registration page with a notifcation about the username/email
        already being used.  How can I do this?'''
    elif rFirstName == "" or rLastName == "" or email == "" or amount == "" or rUsername == "" or rPassword == "" or cPassword == "":
        print("hello");
        return render_template("registration.html", rusername=rUsername, rpassword=rPassword, cpassword=cPassword)
    else:
        if rPassword == cPassword:
            u1 = User(username=rUsername, password_hash=rPassword, email=email, first_name=rFirstName, last_name=rLastName)
            a1 = Account(balance=amount)

            db.session.add(u1)
            db.session.add(a1)

            u1.account = a1

            db.session.commit()
            print("Added user to database")
        else:
            # don't reload cPassword because the passwords did not match
            return render_template("registration.html", rusername=rUsername, rpassword=rPassword, rfirstname=rFirstName, rlastname=rLastName, email=email, amount=amount)
            '''TODO: Add notification saying the passwords do not match'''
    return render_template("homepage.html")

@app.route("/delete_account/")
def delate_account():
    if "username" in session:
        user = User.query.get(1)
        for u in User.query.all():
            if u.username == session["username"]:
                for transaction in u.account.transactions:
                    db.session.delete(transaction)
                db.session.delete(u.account)
                db.session.delete(u)
                return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

# Redirects user to Tracker page.
@app.route("/tracking/", methods=["GET"])
def trackerRedirect():
    return render_template("tracker.html")

# Redirects user to Budget page.
@app.route("/budgeting/", methods=["GET"])
def budgetRedirect():
    return render_template("budgetTool.html")

# Redirects user to Prediction page.
@app.route("/predicting/", methods=["GET"])
def predictionRedirect():
    return render_template("predictionTool.html")

# CLI Commands
@app.cli.command("initdb")
def init_db():
    """Initializes database and any model objects necessary for assignment"""
    db.drop_all()
    db.create_all()

    print("Initialized Cashify Database.")


@app.cli.command("devinit")
def init_dev_data():
    """Initializes database with data for development and testing"""
    db.drop_all()
    db.create_all()

    print("Initialized Cashify Database.")
    a1 = Account(balance=0.00)
    u1 = User(username="Tyler", password_hash="Vogel")
    a2 = Account(balance=0.00)
    u2 = User(username="Brian", password_hash="Torpey")

    db.session.add(a1)
    db.session.add(u1)
    db.session.add(a2)
    db.session.add(u2)

    u1.account = a1
    u2.account = a2

    db.session.commit()
    print("Added dummy data.")


# needed to use sessions
# note that this is a terrible secret key
app.secret_key = "mySecret"

if __name__ == "__main__":
    app.run(threaded=True)