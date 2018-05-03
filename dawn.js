var loggedIn;
var username;
var postingKey;

//LOGIN LOGOUT FUNCTIONS
function checkLoggedIn() {
	var button = document.getElementById('loginlogout');
	var user_label = document.getElementById('user_label');
	var login_form = document.getElementById('login_form');
	var register_form = document.getElementById('register_form');

	//get username/key
	username = getCookie('username');
	postingKey = getCookie('postingKey');

	//alert(username);
	
	if (username === "" || postingKey === ""){
		loggedIn=false;
		button.innerHTML = "Login";
		user_label.innerHTML='';
		user_label.style.visibility='hidden';
		login_form.style.visibility='visible';
		register_form.style.visibility='hidden';
	}else{
		loggedIn = true;
		button.innerHTML = "Logout";
		user_label.innerHTML = username;
		user_label.style.visibility='visible';
		login_form.style.visibility='hidden';
		register_form.style.visibility='visible';
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
		//login_form.style.height=0;
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
	var check = steem.auth.isWif(pkey);
	console.log(check)

	loggedIn = true;
	username = uname;
	postingKey = pkey;
	setCookie('username',uname,365);
	setCookie('postingKey',pkey,365);
	//dont forget to clear these values...
	document.getElementById('username_input').value = "";
	document.getElementById('postingkey_input').value = "";

	checkLoggedIn();
}


//STEEM STUFF
function setupTestnet(){
	//var steem = require('steem');
	steem.config.set('websocket','wss://testnet.steem.vc')
	steem.api.setOptions({ url: 'wss://testnet.steem.vc'});	
	steem.config.set('address_prefix', 'STX')
	steem.config.set('chain_id', '79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673')

	
	//steem.api.getAccounts(['tiagotest'],function(err,result){
		//console.log(err,result);
	//});
	//steem.api.lookupAccountNames(['tiagotest','tiago'], function(err, result) {
		//console.log(err, result);
	//});	
}

//LISTING ASSETS
//REGISTERING ASSETS

// AUTOEXECUTE
checkLoggedIn();
//assign functions to events
document.getElementById("loginlogout").addEventListener('click',click_login_button);//this is the navbar button
document.getElementById("login_form").addEventListener('click',login); //this is the login form button

setupTestnet();
