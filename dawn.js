var loggedIn;
var username;
var postingKey;

//LOGIN LOGOUT FUNCTIONS
function checkLoggedIn() {
	var button = document.getElementById('loginlogout');
	var user_label = document.getElementById('user_label');

	//get username/key
	username = getCookie('username');
	postingKey = getCookie('postingKey');

	//alert(username);
	
	if (username === ""){
		loggedIn=false;
		button.innerHTML = "Login";
		user_label.innerHTML='';
		user_label.style.visibility='hidden';
	}else{
		loggedIn = true;
		button.innerHTML = "Logout";
		user_label.innerHTML = username;
		user_label.style.visibility='visible';
	}
}

function setCookie(cookie_name, cookie_value, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cookie_name + "=" + cookie_value + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function click_login_button(){//on load of the button
	if(loggedIn){
		logout();
	}else{
		login();
	}
}

function logout(){
	loggedIn = false;
	setCookie('username',"",-365);
	setCookie('postingKey',"",-365);
	checkLoggedIn();
}
function login(){
	loggedIn = true;
	//set to predefined 
	setCookie('username','tiagotest',365);
	setCookie('postingKey','tiagotest',365);
	checkLoggedIn();
}

checkLoggedIn();

//document.getElementById("loginlogout").addEventListener('load',checkLoggedIn);
document.getElementById("loginlogout").addEventListener('click',click_login_button);


//OTHER ELEMENTS

