
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

function showBudgetCategories() {
    var isChecked = document.getElementById("budgetByCategory").checked;
    if (isChecked) {
        document.getElementById("budgetByCategoryForm").hidden = false;
    }
    else {
        document.getElementById("budgetByCategoryForm").hidden = true;
    }
}

//Sleep Function
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;

function setup() {
    if (budget == true)
    {
        document.getElementById("budgetBtn").addEventListener("click", addBudget, true);
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

function addBudget() {
    var budgetAmount = document.getElementById("budgetAmount").value;
    var budgetByCategory = document.getElementById("budgetByCategory").checked;
    var budgetPiechart;

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

        removeData(budgetPiechart);
        addData(budgetPiechart, tbody, budgetRow);

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

//helper functions for budget pie chart
function removeData(chart){
    console.log(chart.data.datasets[0].data);
    while(chart.data.labels.length > 0)
        chart.data.labels.pop();
    while(chart.data.datasets[0].data.length > 0)
        chart.data.datasets[0].data.pop();
    chart.update();
    console.log(chart.data.datasets[0].data);
}

function addData(chart, body, headers){
    while(body.length > 0){
        var category = body.shift();
        chart.data.labels.push(category);
        var rows = headers.shift();
        chart.data.datasets[0].data.push(rows);
    }
}

// setup load event
window.addEventListener("load", setup, true);

