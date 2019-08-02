/******************************* Webpage Functions *******************************/
//Needed variables
var transactionArray;
var trackerLine;
var labels = [];
var displayLegend = false;

var categories = ["Other", "Income", "Utilities", "Rent", "Auto", "Education", "Healthcare", "Groceries", "Restaurants", "Home", "Shopping", "Entertainment", "Travel", "Savings"]
var colors = ["rgba(249, 83, 8,", "rgba(249, 204, 8,", "rgba(174, 249, 8,", "rgba(54, 249, 8,", 
                "rgba(54, 249, 8,", "rgba(8, 249, 83,", "rgba(8, 249, 203,", "rgba(8, 174, 249,", 
                "rgba(8, 54, 249,", "rgba(83, 8, 249,", "rgba(172, 8, 249,", 
                "rgba(203, 8, 249,", "rgba(249, 8, 174,", "rgba(249, 8, 54,"];

//Helper Function for plotData
function newDate(days) {
    return moment().add(days, 'd');
}

//Sets up the labes for the current Month
function setLabels() {
    var day = moment().format('D');
    var month = moment().format('M');
    var daysInMonth = 0;
    if(month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12)
        daysInMonth = 31;
    else if(month == 4 || month == 6 || month == 9 || month == 11)
        daysInMonth = 30;
    else
        daysInMonth = 28;      //Leap years don't exist to a programmer

    for(i = 0; i < daysInMonth; i++)
        labels.push(newDate(0 - day + i));
    
}

//Toggles Legend on line graph
function toggleLegend() {
    displayLegend = !displayLegend;
    trackerLine.options.legend.display = displayLegend;
    trackerLine.update();

    if(displayLegend)
        document.getElementById("toggle").innerHTML = "Hide Legend";
    else
        document.getElementById("toggle").innerHTML = "Show Legend";
}

//Changes data on line graph
function dataChange() {
    var value = document.getElementById("dataType").value;
    if("total" != value) {
        removeData(trackerLine);
        for(i = 3; i<transactionArray.length; i++)
            addData(trackerLine, categories[i-3], transactionArray[i], colors[i-3]);
    }
    else {
        removeData(trackerLine);
        addData(trackerLine, "All Transactions", transactionArray[2], "rgba(55, 167, 10,");
    }
}


//Add datasets to the line graph
function addData(chart, label, data, color) {
    var dataset = {
        label: label,
        data: data,
        backgroundColor: color + " 0.2)",
        borderColor: color + " 1)",
        pointBorderColor: color + " 1)",
        pointBackgroundColor: color + " 1)",
        pointBorderColor: color + " 1)",
    }
    chart.data.datasets.push(dataset);
    chart.update();
}

//Clear data to secondary dataset
function removeData(chart) {
    while(chart.data.datasets.length > 0)
        chart.data.datasets.pop();
    chart.update();
}

/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;

function setup() {
        makeReq("GET", "/trackerData", 200, plotData);
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
                //console.log("recieved response text:  " + httpRequest.responseText);
				action(httpRequest.responseText);
			} else {
				alert("There was a problem with the request.  you'll need to refresh the page!");
			}
		}
	}
	return handler;
}


function plotData(responseText) {
    //Collecting data from python
    console.log("populating chart!");
    transactionArray = JSON.parse(responseText);
    if(transactionArray != null) {
        /* Transaction Array = ['All budgets', 'Current Balances', 'All Transactions', 'Income', 'Rent', 'Education', 'Groceries', 'Home Improvement', 'Entertainment', 'Savings', 'Utilities', 'Auto', 'Healthcare', 'Restaurants', 'Shopping', 'Travel', 'Other'] */
        var budgets = transactionArray[0];
        var currBalances = transactionArray[1];
        var allTransactions = transactionArray[2];

        if(budgets != null) {
            for(i = 0; i < budgets.length; i++) {
                if(budgets[i] == null) {
                    currBalances.splice(i, 1);
                    categories.splice(i, 1);
                }
                else
                    currBalances[i] = Math.abs(currBalances[i]);     
            }
        }


        document.getElementById("budgetTitle").innerHTML = "Month of " + moment().format("MMMM");
        setLabels();

        /* Line Graph */
        //Plot Data on line graph using chart.js
        var config = {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                label: "All Transactions",
                data: allTransactions,
                backgroundColor: "rgba(55, 167, 10, 0.2)",
                borderColor: "rgba(55, 167, 10, 1)",
                pointBorderColor: "rgba(55, 167, 10, 1)",
                pointBackgroundColor: "rgba(55, 167, 10, 1)",
                pointBorderColor: "rgba(55, 167, 10, 1)",
                }]
            },
            options: {
                legend: {
                    display: false,
                    labels: {
                        boxWidth: 20,
                        fontSize: 10
                    }
                },
                scaleStartValue: 1,
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: "day",
                            displayFormats: {
                                day: 'MMM D'
                            }
                        }
                    }],
                },
            }
        };
        
        let ctx1 = document.getElementById('trackerChart');
        ctx1.height = 250;

        trackerLine = new Chart(ctx1, config);

        
        /* Bar Graph */
        //Plot Data on Bar Graph with Actual Spending and Goals

        colors1 = []
        colors2 = []
        for(i = 0; i < colors.length; i++) {
            colors1.push(colors[i] + " 0.2)");
            colors2.push(colors[i] + " 1)");
        }
        
        var config = {
            type: 'bar',
            data: {
            labels: categories,
            datasets: [
                {
                    label: "Goal",
                    backgroundColor: colors1,
                    data: budgets,
                    borderColor: "#000",
                    borderWidth: 1
                },
                {
                label: "Deposits/Withdrawls",
                backgroundColor: colors2,
                data: currBalances
                }
            ]
            },
            options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Seperated By Category'
            },
            scales: {
                xAxes: [{
                stacked: true,
                display: false
                }],
                yAxes: [{
                    stacked: false,
                    ticks: {
                    beginAtZero: true
                    },
                }]
            }
            }
        };
        
        let ctx2 = document.getElementById('CategoryBars');
        ctx2.height = 250;


        categoryBars = new Chart(ctx2, config);
    } 
}


/******************************* Webpage Setup *******************************/
// setup load event
window.addEventListener("load", setup, true);