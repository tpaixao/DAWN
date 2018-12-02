<login-button>
	<button if="{ !logged_in }"  class="btn btn-primary" onclick="{ login }">Login</button>

	<ul class="collapse navbar-collapse">
		<li if="{ logged_in }" class="nav-item dropdown">
			<a class="nav-link dropdown-toggle" href="http://example.com" id="dropdown01" data-toggle="dropdown" >{ username }</a>
			<div class="dropdown-menu" >
				<a class="dropdown-item" href="#">My Assets</a>
				<a class="dropdown-item" href="#" onclick="{ logout }">Logout</a>
			</div>
		</li>
	</ul> 

	<style>
	</style>

	<script>
		self	= this;

		check_logged_in() {
			console.log('checking cookie');
			var username  = Cookies.get('username');
			if(username){
				self.username = username;
				return true;
				console.log('found user')
			} else {
				return false;
				console.log('did not find user')
			};
		};

		login(e){
			Cookies.set('username','Tiago');
			console.log('logging in');
			this.logged_in = this.check_logged_in();
			this.update();
		};

		logout(e){
			Cookies.remove('username');
			console.log('logging out');
			this.logged_in = this.check_logged_in();
			this.update();
		};

		this.logged_in=this.check_logged_in();
	</script>

</login-button>
