
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
function addAlert(type, text){
    var parent = document.getElementById("main");
    var firstItem = document.getElementById("finacialTools");
    var alert = document.createElement("div");
    switch(type) {
        case 0:
            alert.setAttribute("class", "alert danger");
        case 1:
            alert.setAttribute("class", "alert warning");
        case 2:
            alert.setAttribute("class", "alert info");
        case 3:
            alert.setAttribute("class", "alert success");
        default:
            alert.setAttribute("class", "alert danger");
    }
    alert.innerHTML += text;

    //Fade out
    setTimeout(function(){ 
        alert.style.opacity = "0";
        setTimeout(function(){ alert.style.display = "none"; }, 600);
    }, 2000)

    parent.insertBefore(alert, firstItem);
}