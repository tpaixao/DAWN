
//main logic

//var mainview;
var contentDiv = document.getElementById('content');
var mainview;

//funcs
function mount_tag(tag,args=''){
	//mainview.unmount();
	contentDiv.innerHTML = '<'+tag+'></'+tag+'>';
	mainview = riot.mount('div#content',tag);
}

function checkLoggedIn(){
}

function setupTestnet(){
	//var steem = require('steem');
	steem.config.set('websocket','wss://testnet.steem.vc')
	steem.api.setOptions({ url: 'wss://testnet.steem.vc'});	
	steem.config.set('address_prefix', 'STX')
	steem.config.set('chain_id', '79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673')

	console.log('testnet setup');
	
	//steem.api.getAccounts(['tiagotest'],function(err,result){
		//console.log(err,result);
	//});
	//steem.api.lookupAccountNames(['tiagotest','tiago'], function(err, result) {
		//console.log(err, result);
	//});	
}

var session = {
	init: function(opts){
		loggedIn = false;
		setupTestnet();
	}
};

mount_tag('login-form')



// mount stuff
//riot.mount('login-button');
//riot.mount('sidemenu');
//check if logged in

