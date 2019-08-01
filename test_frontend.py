from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Account, Transaction, Category, Budget
from helper import separateTransactions, predict, checkSign, dateConverter, getLastMonthTransactions, getLastNDays
from datetime import datetime, date, timedelta
import os
import re
import random

app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "cashify.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

'''***********************************************
                RESTful Resources
***********************************************'''
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



# Transaction Resource
# Creates Transactions and Deletes Transactions
class MyTransaction(Resource):
    def delete(self, transaction_id):
        #Update Account Balance
        t = Transaction.query.filter_by(id=transaction_id).first()
        tAccount = Account.query.filter_by(id=t.account.id).first()
        tAccount.balance -= t.amount
        
        #Delete Transaction
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
            removed = 0
            #transactionList will include the information of each transaction. Amount, date, and category. The last object is the user's account at that moment.
            for t in transactions:
                #Include the last 30 transactions
                if(len(transactions) - removed < 31):
                    transactionList.append(t.date)
                    transactionList.append(t.amount)
                    transactionList.append(t.category)
                    transactionList.append(t.current_balance)
                    transactionList.append(t.id)
                else:
                    removed += 1
            return transactionList
        else:
            return None

    def post(self):
        args = parser.parse_args() 
        amount = args['Amount']      
        category = args['Category']

        #Not a valid float
        if re.match("^-*\d+\.*\d*$", amount) is None:
            return "Invalid", 201

        # Get the user
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        # Correcting the sign of the transaction
        sign = checkSign(category)
        if(sign == -1 and amount[:1] == "-"):
            amount = float(amount)
        else:
            amount = float(amount)*sign

        account = user.account
        transactions = account.transactions
        tempBalance = account.balance + float(amount)
        account.balance = round(tempBalance, 2)
        balance = account.balance 


        dateX = datetime.now()
        date = dateConverter(dateX)

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
            budgetList.append(budget.utilities)
            budgetList.append(budget.rent)
            budgetList.append(budget.auto_gas)
            budgetList.append(budget.education)
            budgetList.append(budget.healthcare)
            budgetList.append(budget.groceries)
            budgetList.append(budget.restaurants)
            budgetList.append(budget.home_improvement)
            budgetList.append(budget.shopping)
            budgetList.append(budget.entertainment)
            budgetList.append(budget.travel)
            budgetList.append(budget.savings)
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

# Prediction Resource
# Creates prediction data to be sent to javascript
class MyPrediction(Resource):
    def get(self):
        #User Information
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        transactions = account.transactions
        balance = account.balance

        #Retrieve the linear prediction
        linearEqn = predict(transactions)

        #Retrieve the past 10 days of balance transformation
        past10DaysBalance = getLastNDays(transactions, balance, 10)

        predictionResponse = [linearEqn[0], linearEqn[1], past10DaysBalance]

        return predictionResponse


# Tracker Resource
# Creates tracker data to be sent to javascript
class MyTracker(Resource):
    def get(self):
        #User Information
        username = session["username"]

        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        transactions = account.transactions
        balance = account.balance
        
        #Seperate the Trasactions
        # Transaction Array = ['Total Budget', 'Income', 'Rent', 'Education', 'Groceries', 'Home Improvement', 'Entertainment', 'Savings', 'Utilities', 'Auto', 'Healthcare', 'Restaurants', 'Shopping', 'Travel', 'Other']
        categories = ["other", "income", "utilities", "rent", "auto", "education", "healthcare", "groceries", "restaurants", "home", "shopping", "entertainment", "travel", "savings"]
        transactionArray = separateTransactions(transactions, categories)

        #Retrieve the past transactions in this month
        pastMonthTransactions = [getLastMonthTransactions(t) for t in transactionArray[1:]]
        pastMonthTransactions.insert(0, transactions)

        #Set up balances
        balances = []
        balances.append(round(balance, 2))
        for ta in pastMonthTransactions[1:]:    #Skip the first one
            tSum = 0
            if(ta != None):
                for t in ta:
                    tSum += t.amount
            balances.append(round(tSum, 2))

        #Gather the data points
        now = datetime.now().date()
        firstDayOfMonth = date(now.year, now.month, 1)

        userBudget = account.budget

        #Get User's budgets
        budgets = [ userBudget.other,  userBudget.income,  userBudget.utilities,  userBudget.rent, \
             userBudget.auto_gas,  userBudget.education,  userBudget.healthcare,  userBudget.groceries, \
                 userBudget.restaurants,  userBudget.home_improvement,  userBudget.shopping,  userBudget.entertainment, \
                     userBudget.travel,  userBudget.savings]

        #Gather the data points for each category
        balanceIterator = 0
        trackerResponse = []
        trackerResponse.append(budgets)
        trackerResponse.append(balances[1:])
        for t in pastMonthTransactions:
            trackerResponse.append(getLastNDays(t, balances[balanceIterator], abs(now-firstDayOfMonth).days))
            balanceIterator+=1

        return trackerResponse


##
## Actually setup the Api resource routing here
##
api.add_resource(TransactionList, '/transactions')
api.add_resource(MyTransaction, '/transactions/<transaction_id>')
api.add_resource(UserBudget, '/budget')
api.add_resource(MyPrediction, '/predictionData')
api.add_resource(MyTracker, '/trackerData')



'''***********************************************
                Webpage Redirects
***********************************************'''
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
            return render_template("homepage.html", alert=True)
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
        return render_template("homepage.html", alert=True)

# Registration of new user
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
        return render_template("registration.html", rusername=rUsername, rpassword=rPassword, cpassword=cPassword, alert1=True)
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
            return render_template("registration.html", rusername=rUsername, rpassword=rPassword, rfirstname=rFirstName, rlastname=rLastName, email=email, amount=amount, alert2=True)
            '''TODO: Add notification saying the passwords do not match'''
    return render_template("homepage.html", success=True)

@app.route("/delete_account/")
def delete_account():
    if "username" in session:
        user = User.query.get(1)
        for u in User.query.all():
            if u.username == session["username"]:
                for transaction in u.account.transactions:
                    db.session.delete(transaction)
                db.session.delete(u.account)
                db.session.delete(u)
                db.session.commit()

                return redirect(url_for("unlogger"))
    else:
        return redirect(url_for("home"))

# Redirects user to Tracker page.
@app.route("/tracking/", methods=["GET"])
def trackerRedirect():
    if "username" in session:
        return render_template("tracker.html")
    else:
        return redirect(url_for("home"))

# Redirects user to Budget page.
@app.route("/budgeting/", methods=["GET"])
def budgetRedirect():
    if "username" in session:
        username = session["username"]
        user = User.query.get(1)
        for u in User.query.all():
            if u.username == username:
                user = u

        account = user.account
        budget = account.budget
        return render_template("budgetTool.html", budget=budget)
    else:
        return redirect(url_for("home"))

# Redirects user to Prediction page.
@app.route("/predicting/", methods=["GET"])
def predictionRedirect():
    if "username" in session:
        return render_template("predictionTool.html")
    else:
        return redirect(url_for("home"))






'''***********************************************
                CLI Commands
***********************************************'''
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
    a1 = Account(balance=400.00)
    u1 = User(username="Tyler", password_hash="Vogel")
    a2 = Account(balance=0.00)
    u2 = User(username="Brian", password_hash="Torpey")

    db.session.add(a1)
    db.session.add(u1)
    db.session.add(a2)
    db.session.add(u2)

    u1.account = a1
    u2.account = a2

    # Transaction dummy data for Tyler
    balance = 400.00
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t1 = Transaction(amount=amount, date="2019-05-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t1)
    a1.transactions.append(t1)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t2 = Transaction(amount=amount, date="2019-05-11", category="Income", current_balance=round(balance, 2))
    db.session.add(t2)
    a1.transactions.append(t2)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t3 = Transaction(amount=amount, date="2019-06-11", category="Entertainment", current_balance=round(balance, 2))
    db.session.add(t3)
    a1.transactions.append(t3)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t4 = Transaction(amount=amount, date="2019-06-11", category="Restaurants", current_balance=round(balance, 2))
    db.session.add(t4)
    a1.transactions.append(t4)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t5 = Transaction(amount=amount, date="2019-06-11", category="Restaurants", current_balance=round(balance, 2))
    db.session.add(t5)
    a1.transactions.append(t5)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t6 = Transaction(amount=amount, date="2019-07-04", category="Savings", current_balance=round(balance, 2))
    db.session.add(t6)
    a1.transactions.append(t6)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t7 = Transaction(amount=amount, date="2019-07-06", category="Income", current_balance=round(balance, 2))
    db.session.add(t7)
    a1.transactions.append(t7)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t8 = Transaction(amount=amount, date="2019-07-08", category="Other", current_balance=round(balance, 2))
    db.session.add(t8)
    a1.transactions.append(t8)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t9 = Transaction(amount=amount, date="2019-07-10", category="Groceries", current_balance=round(balance, 2))
    db.session.add(t9)
    a1.transactions.append(t9)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t10 = Transaction(amount=amount, date="2019-07-12", category="Utilities", current_balance=round(balance, 2))
    db.session.add(t10)
    a1.transactions.append(t10)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t11 = Transaction(amount=amount, date="2019-07-14", category="Other", current_balance=round(balance, 2))
    db.session.add(t11)
    a1.transactions.append(t11)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t12 = Transaction(amount=amount, date="2019-07-15", category="Other", current_balance=round(balance, 2))
    db.session.add(t12)
    a1.transactions.append(t12)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t13 = Transaction(amount=amount, date="2019-07-16", category="Income", current_balance=round(balance, 2))
    db.session.add(t13)
    a1.transactions.append(t13)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t14 = Transaction(amount=amount, date="2019-07-18", category="Entertainment", current_balance=round(balance, 2))
    db.session.add(t14)
    a1.transactions.append(t14)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t15 = Transaction(amount=amount, date="2019-07-19", category="Other", current_balance=round(balance, 2))
    db.session.add(t15)
    a1.transactions.append(t15)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t16 = Transaction(amount=amount, date="2019-07-19", category="Auto", current_balance=round(balance, 2))
    db.session.add(t16)
    a1.transactions.append(t16)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t17 = Transaction(amount=amount, date="2019-07-20", category="Income", current_balance=round(balance, 2))
    db.session.add(t17)
    a1.transactions.append(t17)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t18 = Transaction(amount=amount, date="2019-07-22", category="Healthcare", current_balance=round(balance, 2))
    db.session.add(t18)
    a1.transactions.append(t18)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t19 = Transaction(amount=amount, date="2019-07-22", category="Restaurants", current_balance=round(balance, 2))
    db.session.add(t19)
    a1.transactions.append(t19)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t20 = Transaction(amount=amount, date="2019-07-23", category="Other", current_balance=round(balance, 2))
    db.session.add(t20)
    a1.transactions.append(t20)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t21 = Transaction(amount=amount, date="2019-07-24", category="Other", current_balance=round(balance, 2))
    db.session.add(t21)
    a1.transactions.append(t21)

    a1.balance = balance


    #Setup Budget
    b = Budget(income = 1000, rent = 200, education = 100, groceries = 50, 
    home_improvement = 50, entertainment = 75, savings = 100, utilities = 25, \
    auto_gas = 50, healthcare = 50, restaurants = 50, shopping = 50, travel = 100, other = 200)

    a1.budget = b

    db.session.commit()
    print("Added dummy data.")


# needed to use sessions
# note that this is a terrible secret key
app.secret_key = "mySecret"

if __name__ == "__main__":
    app.run(threaded=True)