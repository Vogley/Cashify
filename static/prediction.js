/******************************* Webpage Functions *******************************/
function newDate(days) {
    return moment().add(days, 'd');
}


/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;

function setup() {
        makeReq("GET", "/predictionData", 200, plotData);
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
    var response = JSON.parse(responseText);   //Should be an array of 3 items: slope, yintercept, and past 10 days of transactions
    var slope = response[0], yintercept = response[1];
    var dataPoints = [null, null, null, null, null, null, null, null, null, null, null];
    var labels = [newDate(-10), newDate(-9), newDate(-8), newDate(-7), newDate(-6), newDate(-5), newDate(-4), newDate(-3), newDate(-2), newDate(-1), newDate(0)]

    //Only show prediction if there is valid data
    if(response[0] != null) {
        for(i = 0; i < 11; i++)
            dataPoints[i] = (slope*i + yintercept).toFixed(2);
    }

    dataTransactions = response[2];
    dataPrediction = [null, null, null, null, null, null, null, null, null, null];

    //Setup chart labels
    for(n = 0; n < 11; n++) {
        if(n > 0)
            labels.push(newDate(n));
        dataPrediction.push(dataPoints[n]);
    }   


    //Plot Data on chart using chart.js
    var config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
            label: "Transactions",
            data: dataTransactions,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            pointBorderColor: "rgba(255, 0, 0, 1)",
            pointBackgroundColor: "rgba(255, 99, 132, 1)",
            pointBorderColor: "rgba(255, 0, 0, 1)",
            }, 
            {
            label: "Prediction",
            data: dataPrediction,
            backgroundColor: "rgba(99, 164, 255, 0.2)",
            borderColor: "rgba(99, 164, 255, 1)",
            pointBorderColor: "rgba(0, 0, 255, 1)",
            pointBackgroundColor: "rgba(99, 164, 255, 1)",
            pointBorderColor: "rgba(0, 0, 255, 1)",
            }]
        },
        options: {
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
    
    let ctx = document.getElementById('predictionChart');
    
    //Dynamic height 
    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    if(w < 450)
        ctx.height = 300;
    else
        ctx.height = 200;
    let budgetChart = new Chart(ctx, config);
}

/******************************* Webpage Setup *******************************/
// setup load event
window.addEventListener("load", setup, true);