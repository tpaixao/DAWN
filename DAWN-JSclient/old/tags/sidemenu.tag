<sidemenu>
	<!-- spacer-->
	<div style="overflow: hidden;height: 50px;"></div> 
	<!-- buttons -->
  <div>
    <span class="stack pseudo button"><a onclick={ this.change_view } view='asset-list' vals='' >My Assets</a></span>
		<span class="stack pseudo button"><a onclick={ this.change_view } view='search-panel' vals='' >Search Assets</a></span>
		<span class="stack pseudo button"><a onclick={ this.change_view } view='register-panel' vals='' >Register Asset</a></span>
  </div>

	//this.mixin(session);
	change_view(e){
	//	unmount_main_view();
		console.log('changing view');
		console.log(e.target.attributes.view.value);
		var view = e.target.attributes.view.value; 
		var vals = e.target.attributes.vals.value;
		mount_tag(view);
	}

</sidemenu>
