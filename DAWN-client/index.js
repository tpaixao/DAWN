
//main logic

//var mainview;
var contentDiv = document.getElementById('content');
var mainview;

//funcs
//function unmount_main_view() {
	//mainview.unmount();
//}
function mount_tag(tag,args){
	//mainview.unmount();
	contentDiv.innerHTML = '<'+tag+'></'+tag+'>';
	mainview = riot.mount('div#content',tag);
}



mount_tag('login-form')

// mount stuff
//riot.mount('login-button');
//riot.mount('sidemenu');
//check if logged in

