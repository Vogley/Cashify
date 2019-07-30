
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

/* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
    } else {
        dropdownContent.style.display = "block";
    }
  });
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

//Alert Button Setup. Type = 0 for danger, 1 for warning, 2 for info, 3 for success
function addAlert(type, text, firstItemID){
    var parent = document.getElementById("main");
    var firstItem = document.getElementById(firstItemID);
    var alert = document.createElement("div");
    if(type == 0)
        alert.setAttribute("class", "alert danger");
    else if(type == 1)
        alert.setAttribute("class", "alert warning");
    else if(type == 2)
        alert.setAttribute("class", "alert info");
    else
        alert.setAttribute("class", "alert success");
    alert.innerHTML += text;
    //Fade out
    setTimeout(function(){ 
        alert.style.opacity = "0";
        setTimeout(function(){ alert.style.display = "none"; }, 600);
    }, 2000)

    parent.insertBefore(alert, firstItem);
}
