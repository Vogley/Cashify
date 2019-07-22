from flask import Flask, request, session, render_template, abort, redirect, url_for, flash, make_response
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Account, Transaction
from datetime import datetime, date, timedelta
import os
import re
import random

app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "connect4.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


'''*****RESTful Resources*****'''
parser = reqparse.RequestParser()
parser.add_argument('Amount')
parser.add_argument('Category')


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


##
## Actually setup the Api resource routing here
##
api.add_resource(TransactionList, '/transactions')
api.add_resource(MyTransaction, '/transactions/<transaction_id>')
api.add_resource(MyPrediction, '/predictionData')




'''*****Webpage Redirections*****'''
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
    if "username" in session:
        return render_template("tracker.html")
    else:
        return redirect(url_for("home"))

# Redirects user to Budget page.
@app.route("/budgeting/", methods=["GET"])
def budgetRedirect():
    if "username" in session:
        return render_template("budgetTool.html")
    else:
        return redirect(url_for("home"))

# Redirects user to Prediction page.
@app.route("/predicting/", methods=["GET"])
def predictionRedirect():
    if "username" in session:
        return render_template("predictionTool.html")
    else:
        return redirect(url_for("home"))



'''*****Webpage Functionss*****'''
# Function to change a dates format
def dateConverter(o):
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

# Function to check the sign of the category
def checkSign(category):
    firstC = category[:1]
    if(firstC == "i"):      # Income
        return 1
    elif(firstC == "u"):    # Utilities
        return -1
    elif(firstC == "r"):    # Rent or Resturants
        return -1
    elif(firstC == "a"):    # Auto and Gas
        return -1
    elif(firstC == "e"):    # Education or Entertainment
        return -1
    elif(firstC == "h"):    # Healthcare or Home Improvement
        return -1
    elif(firstC == "g"):    # Grocieries
        return -1
    elif(firstC == "s"):    # Shopping or Savings
        secondC = category[:2]
        print(secondC)
        if(secondC == "sh"):
            return -1
        else:
            return 1
    elif(firstC == "t"):    # Traveling
        return -1
    else:                   # Other Cases
        return 1

#Prediciton Algorithm, takes in an account everytime he/she enters in a new transaction
def predict(transactions):
    now = datetime.now().date()
    linearEqn = [None, None]

    tYear, tMonth, tDay = int(transactions[0].date[:4]), int(transactions[0].date[5:7]), int(transactions[0].date[8:])
    oldestDate = date(tYear, tMonth, tDay)

    minDate = now - timedelta(days=40)

    #Transactions has been entered 40 or more days ago. Algorithm can procede
    if(oldestDate < minDate):
        totalSum = 0    #var to keep track of user's balance in the last 40 days
        slope = 0
        yintercept = transactions[len(transactions) - 1].current_balance
        #Process is to take the average growth or decline per day from the last 40 days. Only calculate from last 40 days.
        for t in transactions:
            tempYear, tempMonth, tempDay = int(t.date[:4]), int(t.date[5:7]), int(t.date[8:])
            tDate = date(tempYear, tempMonth, tempDay)
            if(minDate < tDate):
                totalSum += t.amount
            
            slope = round(totalSum/40, 2)

        linearEqn = [slope, yintercept]

    return linearEqn  

#Helper function for creating data points for the last N days
def getLastNDays(transactions, balance, n):
    now = datetime.now().date()
    dateNDaysAgo = now - timedelta(days=n)
    
    #Fill with the n previous dates
    pastNDays = []
    for x in range(n):
        pastNDays.append(now - timedelta(days=n-x))

    pastNDays.append(now)  #For today's datapoint

    #Fill all with the balance of today
    pastNDaysBalance = []
    for y in range(n+1):
        pastNDaysBalance.append(balance)
    
    #Setup the previous n days of transactions
    for t in transactions:
        tempYear, tempMonth, tempDay = int(t.date[:4]), int(t.date[5:7]), int(t.date[8:])
        tDate = date(tempYear, tempMonth, tempDay)
        #Is a valid transaction
        if(tDate > dateNDaysAgo):
            i = 0
            for day in pastNDays:
                if(tDate > day):
                    i += 1
                else:
                    break

            if(i > 0):
                while i > 0:
                    pastNDaysBalance[i-1] -= t.amount
                    pastNDaysBalance[i-1] = round(pastNDaysBalance[i-1], 2)
                    i -= 1

    return pastNDaysBalance
    




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
    t2 = Transaction(amount=amount, date="2019-05-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t2)
    a1.transactions.append(t2)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t3 = Transaction(amount=amount, date="2019-06-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t3)
    a1.transactions.append(t3)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t4 = Transaction(amount=amount, date="2019-06-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t4)
    a1.transactions.append(t4)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t5 = Transaction(amount=amount, date="2019-06-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t5)
    a1.transactions.append(t5)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t6 = Transaction(amount=amount, date="2019-07-04", category="Other", current_balance=round(balance, 2))
    db.session.add(t6)
    a1.transactions.append(t6)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t7 = Transaction(amount=amount, date="2019-07-06", category="Other", current_balance=round(balance, 2))
    db.session.add(t7)
    a1.transactions.append(t7)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t8 = Transaction(amount=amount, date="2019-07-08", category="Other", current_balance=round(balance, 2))
    db.session.add(t8)
    a1.transactions.append(t8)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t9 = Transaction(amount=amount, date="2019-07-10", category="Other", current_balance=round(balance, 2))
    db.session.add(t9)
    a1.transactions.append(t9)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t10 = Transaction(amount=amount, date="2019-07-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t10)
    a1.transactions.append(t10)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t11 = Transaction(amount=amount, date="2019-07-12", category="Other", current_balance=round(balance, 2))
    db.session.add(t11)
    a1.transactions.append(t11)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t12 = Transaction(amount=amount, date="2019-07-12", category="Other", current_balance=round(balance, 2))
    db.session.add(t12)
    a1.transactions.append(t12)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t13 = Transaction(amount=amount, date="2019-07-10", category="Other", current_balance=round(balance, 2))
    db.session.add(t13)
    a1.transactions.append(t13)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t14 = Transaction(amount=amount, date="2019-07-11", category="Other", current_balance=round(balance, 2))
    db.session.add(t14)
    a1.transactions.append(t14)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t15 = Transaction(amount=amount, date="2019-07-12", category="Other", current_balance=round(balance, 2))
    db.session.add(t15)
    a1.transactions.append(t15)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t16 = Transaction(amount=amount, date="2019-07-12", category="Other", current_balance=round(balance, 2))
    db.session.add(t16)
    a1.transactions.append(t16)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t17 = Transaction(amount=amount, date="2019-07-13", category="Other", current_balance=round(balance, 2))
    db.session.add(t17)
    a1.transactions.append(t17)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t18 = Transaction(amount=amount, date="2019-07-13", category="Other", current_balance=round(balance, 2))
    db.session.add(t18)
    a1.transactions.append(t18)
    amount = -round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t19 = Transaction(amount=amount, date="2019-07-14", category="Other", current_balance=round(balance, 2))
    db.session.add(t19)
    a1.transactions.append(t19)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t20 = Transaction(amount=amount, date="2019-07-15", category="Other", current_balance=round(balance, 2))
    db.session.add(t20)
    a1.transactions.append(t20)
    amount = round(random.uniform(1.00, 100.00), 2)
    balance += amount
    t21 = Transaction(amount=amount, date="2019-07-16", category="Other", current_balance=round(balance, 2))
    db.session.add(t21)
    a1.transactions.append(t21)

    a1.balance = balance

    db.session.commit()
    print("Added dummy data.")


# needed to use sessions
# note that this is a terrible secret key
app.secret_key = "mySecret"

if __name__ == "__main__":
    app.run(threaded=True)