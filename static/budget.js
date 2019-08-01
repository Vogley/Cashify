
/******************************* Webpage Functions *******************************/
var nav = false;
var loaded = false;

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

//Sleep Function
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;

function setup() {
    document.getElementById("budgetBtn").addEventListener("click", addBudget, true);
    makeReq("GET", "/budget", 200, plotData);
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
				action(httpRequest.responseText);
			} else {
				alert("There was a problem with the request.  you'll need to refresh the page!");
			}
		}
	}
	return handler;
}

function addBudget() {

    //get category values
    var incomeBudget = document.getElementById("incomeBudget").value != "" ? document.getElementById("incomeBudget").value : 0;
    var utilitiesBudget = document.getElementById("utilitiesBudget").value != "" ? document.getElementById("utilitiesBudget").value : 0;
    var rentBudget = document.getElementById("rentBudget").value != "" ? document.getElementById("rentBudget").value : 0;
    var gasBudget = document.getElementById("gasBudget").value != "" ? document.getElementById("gasBudget").value : 0;
    var educationBudget = document.getElementById("educationBudget").value != "" ? document.getElementById("educationBudget").value : 0;
    var healthBudget = document.getElementById("healthBudget").value != "" ? document.getElementById("healthBudget").value : 0;
    var groceriesBudget = document.getElementById("groceriesBudget").value != "" ? document.getElementById("groceriesBudget").value : 0;
    var restaurantsBudget = document.getElementById("restaurantsBudget").value != "" ? document.getElementById("restaurantsBudget").value : 0;
    var homeBudget = document.getElementById("homeBudget").value != "" ? document.getElementById("homeBudget").value : 0;
    var shoppingBudget = document.getElementById("shoppingBudget").value != "" ? document.getElementById("shoppingBudget").value : 0;
    var entertainmentBudget = document.getElementById("entertainmentBudget").value != "" ? document.getElementById("entertainmentBudget").value : 0;
    var travelBudget = document.getElementById("travelBudget").value != "" ? document.getElementById("travelBudget").value : 0;
    var savingsBudget = document.getElementById("savingsBudget").value != "" ? document.getElementById("savingsBudget").value : 0;
    var otherBudget = document.getElementById("otherBudget").value != "" ? document.getElementById("otherBudget").value : 0;

    var totalBudget = parseFloat(incomeBudget) + parseFloat(utilitiesBudget) + parseFloat(rentBudget) + parseFloat(gasBudget) + parseFloat(educationBudget) +
        parseFloat(healthBudget) + parseFloat(groceriesBudget) + parseFloat(restaurantsBudget) +
        parseFloat(homeBudget) + parseFloat(shoppingBudget) + parseFloat(entertainmentBudget) + parseFloat(travelBudget) + parseFloat(savingsBudget) +
        parseFloat(otherBudget);

    data = "Total Budget=" + totalBudget + "&Income=" + incomeBudget +
    "&Rent=" + rentBudget + "&Education=" + educationBudget + "&Groceries=" +
    groceriesBudget + "&Home Improvement=" + homeBudget + "&Entertainment=" +
    entertainmentBudget + "&Savings=" + savingsBudget + "&Utilities=" + utilitiesBudget +
    "&Auto=" + gasBudget + "&Healthcare=" + healthBudget + "&Restaurants=" + restaurantsBudget +
    "&Shopping=" + shoppingBudget + "&Travel=" + travelBudget + "&Other=" + otherBudget;

    window.clearTimeout(timeoutID);
    makeReq("PUT", "/budget", 201, budgetPoller, data);
}

function budgetPoller() {
    makeReq("GET", "/budget", 200, populateBudget);
}

function populateBudget(responseText) {
        document.getElementById("firstItem").style.display = "block";
        addAlert(2, "Budget Successfully Created.", "firstItem")
        var budgetString = JSON.parse(responseText);

        tbody = document.getElementById("tbody");

        //Header Row
        budgetRow = document.getElementById("budgetRow");

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

                var total = 0;
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
    removeData(budgetChart);
    plotData(budgetString);
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
        chart.data.datasets.pop();
}


function plotData(responseText) {
    if(!loaded)
        var budgetArray = JSON.parse(responseText);
    else 
        var budgetArray = responseText;
    var data = [];

    for(i = 1; i < budgetArray.length; i++)
        data.push(budgetArray[i]);


    var colors = ["rgba(249, 83, 8, 0.5)", "rgba(249, 204, 8, 0.5)", "rgba(174, 249, 8, 0.5)", "rgba(54, 249, 8, 0.5)", 
                "rgba(54, 249, 8, 0.5)", "rgba(8, 249, 83, 0.5)", "rgba(8, 249, 203, 0.5)", "rgba(8, 174, 249, 0.5)", 
                "rgba(8, 54, 249, 0.5)", "rgba(83, 8, 249, 0.5)", "rgba(172, 8, 249, 0.5)", 
                "rgba(203, 8, 249, 0.5)", "rgba(249, 8, 174, 0.5)", "rgba(249, 8, 54, 0.5)"];
    //Plot Data on chart using chart.js
    var config = {
        type: 'pie',
        data: {
            labels: ['Income', 'Utilities', 'Rent', 'Auto + Gas', 'Education', 'Healthcare', 'Groceries', 'Restauramts', 'Home Improvement', 'Shopping', 'Entertainment', 'Travel', 'Savings', 'Other'],
            datasets: [{
            label: 'Overall Spending',
            data: data,
            backgroundColor: colors
            }] 
        },
        options: {
            legend: {
                display: false,
            }
        }

    };
    
    let ctx = document.getElementById('budgetChart');
    if(!loaded)
        ctx.height = 250;


    budgetChart = new Chart(ctx, config);
    loaded = true;
}

// setup load event
window.addEventListener("load", setup, true);