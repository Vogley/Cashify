
/******************************* Webpage Functions *******************************/
var nav = false;

//Navigation Bar
function toggleNav() {
    if(nav == false)
    {
        document.getElementById("mySidenav").style.transform = "translateX(0)";
        document.getElementById("page-container").style.transform = "translateX(250px)";
        document.getElementById("titleBar").style.transform = "translateX(250px)";
    }
    else
    {
        document.getElementById("mySidenav").style.transform = "translateX(-250px)";
        document.getElementById("page-container").style.transform = "translateX(0)";
        document.getElementById("titleBar").style.transform = "translateX(0)";
    }
    nav = !nav;
}

//Scroll Functions
async function scrollToTop(){
    // Scroll to a certain element
    document.querySelector('#page-container').scrollIntoView({ 
        behavior: 'smooth' 
    });
    await sleep(300);
    toggleNav();
}

async function scrollToLogin(){
    // Scroll to a certain element
    document.querySelector('#form-container').scrollIntoView({ 
        behavior: 'smooth' 
    });
    await sleep(300);
    toggleNav();
}

function checkOther(){
    var selectVal = document.getElementById("category").value;
    if(selectVal == "newCategory")
    {
        document.getElementById("newCategory").disabled = false;
        document.getElementById("newCategory").style.display = "block";
    }
    else
    {
        document.getElementById("newCategory").disabled = true;
        document.getElementById("newCategory").style.display = "none";
    }
}

function showBudgetCategories() {
    var isChecked = document.getElementById("budgetByCategory").checked;
    if (isChecked) {
        document.getElementById("budgetByCategoryForm").hidden = false;
    }
    else {
        document.getElementById("budgetByCategoryForm").hidden = true;
    }
}

//Pop-Up function
function infoPopUp() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

function infoPopOff() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

//Sleep Function
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;

function setup() {
    if(home == true)
    {
        document.getElementById("transactionBtn").addEventListener("click", addTransaction, true);
        poller();
    }
    if (budget == true)
    {
        document.getElementById("budgetBtn").addEventListener("click", addBudget, true);
        budgetPoller();
    }
}

function makeReq(method, target, retCode, action, data) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, action);
	httpRequest.open(method, target);
	
	if (data){
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		httpRequest.send(data);
	}
	else {
		httpRequest.send();
	}
}

function makeHandler(httpRequest, retCode, action) {
	function handler() {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			if (httpRequest.status === retCode) {
				console.log("recieved response text:  " + httpRequest.responseText);
				action(httpRequest.responseText);
			} else {
				alert("There was a problem with the request.  you'll need to refresh the page!");
			}
		}
	}
	return handler;
}


function addTransaction() {
    var amount = document.getElementById("transactionAmount").value;
    var category = document.getElementById("category").value;
    if(category === "newCategory") {
        var newCategory = document.getElementById("newCategory").value;
        data = "Amount=" + amount + "&Category=" + newCategory;
        //Will add functionality to new category later
    }
    else {
        data = "Amount=" + amount + "&Category=" + category;
    }
    window.clearTimeout(timeoutID);
    makeReq("POST", "/transactions", 201, poller, data);
}

function addBudget() {
    var budgetAmount = document.getElementById("budgetAmount").value;
    var budgetByCategory = document.getElementById("budgetByCategory").checked;

    //get category values
    var incomeBudget = document.getElementById("incomeBudget").value;
    var utilitiesBudget = document.getElementById("utilitiesBudget").value;
    var rentBudget = document.getElementById("rentBudget").value;
    var gasBudget = document.getElementById("gasBudget").value;
    var educationBudget = document.getElementById("educationBudget").value;
    var healthBudget = document.getElementById("healthBudget").value;
    var groceriesBudget = document.getElementById("groceriesBudget").value;
    var restaurantsBudget = document.getElementById("restaurantsBudget").value;
    var homeBudget = document.getElementById("homeBudget").value;
    var shoppingBudget = document.getElementById("shoppingBudget").value;
    var entertainmentBudget = document.getElementById("entertainmentBudget").value;
    var travelBudget = document.getElementById("travelBudget").value;
    var savingsBudget = document.getElementById("savingsBudget").value;
    var otherBudget = document.getElementById("otherBudget").value;
    if(budgetByCategory) {

        data = "Total Budget=" + budgetAmount + "&Income=" + incomeBudget +
        "&Rent=" + rentBudget + "&Education=" + educationBudget + "&Groceries=" +
        groceriesBudget + "&Home Improvement=" + homeBudget + "&Entertainment=" +
        entertainmentBudget + "&Savings=" + savingsBudget + "&Utilities=" + utilitiesBudget +
        "&Auto=" + gasBudget + "&Healthcare=" + healthBudget + "&Restaurants=" + restaurantsBudget +
        "&Shopping=" + shoppingBudget + "&Travel=" + travelBudget + "&Other=" + otherBudget;
        //Will add functionality to new category later
    }
    else {
        data = "Total Budget=" + budgetAmount;
    }
    window.clearTimeout(timeoutID);
    makeReq("PUT", "/budget", 201, budgetPoller, data);
}

function poller() {
	makeReq("GET", "/transactions", 200, repopulate);
}

function budgetPoller() {
    makeReq("GET", "/budget", 200, populateBudget);
}

function populateBudget(responseText) {
    if (budget == true)
    {
        console.log("repopulating!");
        var budgetString = JSON.parse(responseText);
        console.log(budgetString);

        tbody = document.getElementById("tbody");

        //Header Row
        budgetRow = document.getElementById("budgetRow");

        //addCells("th", newRow, "Date", "Amount", "Category", "Balance");
        //thead.appendChild(newRow);

        // remove current budget
        while (budgetRow.firstChild) {
            budgetRow.removeChild(budgetRow.firstChild);
        }

        // get rid of create a budget text
        if (budgetString != null) {
            if (budgetString[1] == null) {
                // hide all table headers that aren't the total amount column
                var categoryHeaders = document.getElementsByClassName("categoryBudget");
                for (var i = 0; i < categoryHeaders.length; i++) {
                    categoryHeaders[i].hidden = true;
                }
                var totalBudget = document.createElement("td");

                var tmp = String(budgetString[0]);

                // format budget nicely
                if(tmp.indexOf('.') == -1)
                    tmp = tmp + ".00";
                if(tmp.indexOf('.') != -1 && tmp.length == tmp.indexOf('.') + 2)
                    tmp = tmp + "0";
                totalBudget.innerHTML = "$" + tmp;

                budgetRow.appendChild(totalBudget);

            }
            else {
                // show all table headers
                var categoryHeaders = document.getElementsByClassName("categoryBudget");
                for (var i = 0; i < categoryHeaders.length; i++) {
                    categoryHeaders[i].hidden = false;
                }
                for (var i = 0; i < budgetString.length; i++) {
                    var e = document.createElement("td");

                    var tmp = String(budgetString[i]);

                    // format budget nicely

                    if(tmp.indexOf('.') == -1)
                        tmp = tmp + ".00";
                    if(tmp.indexOf('.') != -1 && tmp.length == tmp.indexOf('.') + 2)
                        tmp = tmp + "0";

                    e.innerHTML = "$" + tmp;

                    budgetRow.appendChild(e);
                }
            }
        }
        else {
            var createBudgetText = document.createElement("td");
            createBudgetText.innerHTML = "Create a budget above...";
            createBudgetText.setAttribute("colspan", "15");
            budgetRow.appendChild(createBudgetText);
        }

    }
}

function deleteTransaction(transactionID) {
	makeReq("DELETE", "/transactions/" + transactionID, 204, poller);
}

// helper function for repop:
function addCells(e, row, cell1, cell2, cell3, cell4) {
    var h1 = document.createElement(e)
    var h2 = document.createElement(e)
    var h3 = document.createElement(e)
    var h4 = document.createElement(e)

    h1.innerHTML = cell1;
    h2.innerHTML = cell2;
    h3.innerHTML = cell3;
    h4.innerHTML = cell4;
    
    row.appendChild(h1);
    row.appendChild(h2);
    row.appendChild(h3);
    row.appendChild(h4);
}

function repopulate(responseText) {
    if(home == true)
    {
        console.log("repopulating!");
        var transactionList = JSON.parse(responseText);
        var tab = document.getElementById("transactionTable");
        var thead, tbody, newRow;
        var tempDate, tempAmount, tempCategory, tempBalance, transactionDate, transactionAmount, transactionCategory, transactionBalance;

    
        while (tab.rows.length > 0) {
            tab.deleteRow(0);
        }

        thead = document.getElementById("thead");
        tbody = document.getElementById("tbody");
        
        //Header Row
        newRow = document.createElement("tr");
        newRow.setAttribute("class", "style3");
        
        addCells("th", newRow, "Date", "Amount", "Category", "Balance");
        thead.appendChild(newRow);

        if(transactionList != null)
        {
            //The transactionlist is one huge string atm. A split can seperate them
            for (i = transactionList.length-4; i >= 0; i-=4) {
                //Body Rows
                newRow = document.createElement("tr");
                
                //Date Formatted
                tempDate = new Date(transactionList[i]);
                transactionDate = tempDate.toDateString().substring(3, tempDate.toDateString().length);

                //Amount Formatted
                tempAmount = String(transactionList[i + 1]);
                if(tempAmount.indexOf('.') == -1)
                    tempAmount = tempAmount + ".00";
                if(tempAmount.indexOf('.') != -1 && tempAmount.length == tempAmount.indexOf('.') + 2)
                    tempAmount = tempAmount + "0";
                transactionAmount = "$" + tempAmount;

                //Category Formatted
                tempCategory = transactionList[i + 2];
                letter = tempCategory.charAt(0);
                transactionCategory = letter.toUpperCase() + tempCategory.substring(1, tempCategory.length);

                //Balance Formatted
                tempBalance = String(transactionList[i + 3]);
                if(tempBalance.indexOf('.') == -1)
                    tempBalance = tempBalance + ".00";
                if(tempBalance.indexOf('.') != -1 && tempBalance.length == tempBalance.indexOf('.') + 2)
                    tempBalance = tempBalance + "0";
                transactionBalance = "$" + tempBalance;
                
                addCells("td", newRow, transactionDate, transactionAmount, transactionCategory, transactionBalance);
                tbody.appendChild(newRow)
            }
        }
    
        timeoutID = window.setTimeout(poller, timeout);
    }

}

function addBudgetInfo(e, row, cell1, cell2, cell3, cell4) {
    var h1 = document.createElement(e)
    var h2 = document.createElement(e)
    var h3 = document.createElement(e)
    var h4 = document.createElement(e)

    h1.innerHTML = cell1;
    h2.innerHTML = cell2;
    h3.innerHTML = cell3;
    h4.innerHTML = cell4;

    row.appendChild(h1);
    row.appendChild(h2);
    row.appendChild(h3);
    row.appendChild(h4);
}


// setup load event
window.addEventListener("load", setup, true);