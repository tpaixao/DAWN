<sidemenu>
	<!-- spacer-->
	<div style="overflow: hidden;height: 50px;"></div> 
	<!-- buttons -->
  <div>
    <span class="stack pseudo button"><a onclick={ this.change_view }>My Assets</a></span>
		<span class="stack pseudo button">Search Assets</span>
		<span class="stack pseudo button">Register Asset</span>
  </div>

	//this.mixin(session);
	change_view(){
	//	unmount_main_view();
		console.log('changing view');
		mount_tag('asset-list');
	}

</sidemenu>
