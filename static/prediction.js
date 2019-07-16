/******************************* This is RESTful JS *******************************/
var home = ture;
var timeoutID;
var timeout = 1000;

function setup() {
    if(home == true)
    {
        makeReq("GET", "/predictionData", 200, plotData);
        poller();
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
    console.log("populating!");
    var linearEqn = JSON.parse(responseText);   //Should be an array of 5 items: slope, yintercept, year, month, and day of the last transaction
    var slope = linearEqn[0], yintercept = linearEqn[1], year = linearEqn[2], month = linearEqn[3], day = linearEqn[4];
    var dataPoints = {}
    


    for( var i = 0; i < 10; i++)
        dataPoints[]
        
}


/******************************* Webpage Setup *******************************/
// setup load event
window.addEventListener("load", setup, true);