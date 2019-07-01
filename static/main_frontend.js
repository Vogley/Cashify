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