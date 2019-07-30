/******************************* This is RESTful JS *******************************/
var timeoutID;
var timeout = 1000;
var lastTransactionID = 0;

function setup() {
    document.getElementById("transactionBtn").addEventListener("click", addTransaction, true);
    poller();
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
                if(httpRequest.responseText.includes("Invalid"))    // User made a bad transaction post
                    badPost();
                else
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

function poller() {
	makeReq("GET", "/transactions", 200, repopulate);
}

function deleteTransaction() {
    makeReq("DELETE", "/transactions/" + lastTransactionID, 204, poller);
    addAlert(2, "Deleted Previous Transaction.");
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
        for (i = transactionList.length-5; i >= 0; i-=5) {
                
            //Body Rows
            newRow = document.createElement("tr");
                
            //Date Formatted
            tempDate = new Date(transactionList[i].substring(0, 4), transactionList[i].substring(5, 7)-1, transactionList[i].substring(8, 10));  //Remember that javascript Date have months start at 0
            transactionDate = tempDate.toDateString().substring(3, tempDate.toDateString().length);

            //Amount Formatted
            tempAmount = String(transactionList[i + 1]);
            if(tempAmount.indexOf('.') == -1)
                tempAmount = tempAmount + ".00";
            if(tempAmount.indexOf('.') != -1 && tempAmount.length == tempAmount.indexOf('.') + 2)
                tempAmount = tempAmount + "0";
            if(tempAmount < 0)
                transactionAmount = tempAmount.substring(0,1) + '$' + tempAmount.substring(1, tempAmount.length);
            else
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
                tempBalance = tempBalance + '0';
            if(parseInt(tempBalance) < 0)
                transactionBalance = tempBalance.substring(0,1) + '$' + tempBalance.substring(1, tempBalance.length);
            else
                transactionBalance = '$' + tempBalance;
                
            addCells("td", newRow, transactionDate, transactionAmount, transactionCategory, transactionBalance);
            tbody.appendChild(newRow)
        }
        //Update Delete Btn
        lastTransactionID = transactionList[transactionList.length - 1];
    }
    timeoutID = window.setTimeout(poller, timeout);
}

//Bad Post
function badPost(){
    var transactionInput = document.getElementById("transactionAmount");
    transactionInput.value = "";
    addAlert(0, "Invalid Transaction Value. Please try again.", "finacialTools");
}

/******************************* Webpage Setup *******************************/
// setup load event
window.addEventListener("load", setup, true);

//Delete Btn Set Up
deleteBtn = document.getElementById("deleteBtn");
(function(){ deleteBtn.addEventListener("click", function() { deleteTransaction(); }); })();