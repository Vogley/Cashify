from datetime import datetime, date, timedelta

'''***********************************************
                Webpage Functions
***********************************************'''
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
    elif(firstC == "r"):    # Rent or Restaurants
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
    if(transactions != None):
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
    
    else:
        return None
    
#Helper function for gathering the transactions of the last month
def getLastMonthTransactions(transactions):
    now = datetime.now().date()
    firstDayOfMonth = date(now.year, now.month, 1)
    ret = []

    if(transactions != None):
        #Setup the previous n days of transactions
        for t in transactions:
            tempYear, tempMonth, tempDay = int(t.date[:4]), int(t.date[5:7]), int(t.date[8:])
            tDate = date(tempYear, tempMonth, tempDay)
            #Is a valid transaction
            if(tDate > firstDayOfMonth):
                ret.append(t)
    else:
        ret = None

    return ret


def separateTransactions(transactions, categories):
    transactionArray = []
    #first item is all transactions
    transactionArray.append(transactions)
    for cName in categories:
        currCategory = []
        for t in transactions:
            if t.category.lower() == cName.lower():
                currCategory.append(t)

        if(len(currCategory) > 0):
            transactionArray.append(currCategory)
        else:
            transactionArray.append(None)

    return transactionArray