

function unmount_main_view(){
	mainview.unmount();
}

//main logic
var mainview;

riot.mount('login-button');

mainview = riot.mount('div#content','login-form');

