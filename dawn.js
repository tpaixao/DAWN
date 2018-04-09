var loggedIn;
var username;
var postingKey;

//LOGIN LOGOUT FUNCTIONS
function checkLoggedIn() {
	var button = document.getElementById('loginlogout');
	var user_label = document.getElementById('user_label');
	var login_form = document.getElementById('login_form');
	//get username/key
	username = getCookie('username');
	postingKey = getCookie('postingKey');

	//alert(username);
	
	if (username === ""){
		loggedIn=false;
		button.innerHTML = "Login";
		user_label.innerHTML='';
		user_label.style.visibility='hidden';
		login_form.style.visibility='visible';
	}else{
		loggedIn = true;
		button.innerHTML = "Logout";
		user_label.innerHTML = username;
		user_label.style.visibility='visible';
		login_form.style.visibility='hidden';
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

function click_login_button(){
	if(loggedIn){
		logout();
	}else{
		var login_form = document.getElementById('login_form');
		login_form.style.visibility='visible';
		//login();
	}
}

function logout(){
	loggedIn = false;
	setCookie('username',"",-365);
	setCookie('postingKey',"",-365);
	checkLoggedIn();
}
function login(){
	//set to predefined 
	uname = document.getElementById('username_input').value;
	pkey = document.getElementById('postingkey_input').value;

	//check validity

	loggedIn = true;
	username = uname;
	postingKey = pkey;
	setCookie('username',uname,365);
	setCookie('postingKey',pkey,365);
	//dont forget to clear these values...

	checkLoggedIn();
}

checkLoggedIn();

//assign functions to events
document.getElementById("loginlogout").addEventListener('click',click_login_button);//this is the navbar button
document.getElementById("login_form").addEventListener('click',login); //this is the login form button


//OTHER ELEMENTS

