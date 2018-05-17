<login-form >
	<div id="login_form" class="" style="width: 100%">
		<article class="card">
			<header>
				<h2>Login</h2>
				<fieldset class="flex two">
					<label> <input ref="username_input" type="username" placeholder="STEEM username"></label>
					<label><input ref="postingkey_input" type="password" placeholder="Private Posting Key"></label>
				</fieldset>	
				<a ref="login_button" class="button sucess" onclick={ this.login }>{ label }</a>
			</header>
		</article>

	</div>

	//code
	<script>
	this.label = "Login"

	this.on('mount',function() {
		console.log("mounted")
	});

	keyIsValid(pKey){
		//console.log(steem.auth.isWif(pKey));
		//console.log(steem.auth.wifToPublic(pKey));
		//console.log(pKey);
		//console.log(steem.auth.wifIsValid(pKey,steem.auth.wifToPublic(pKey)));
		var pubKey =steem.auth.wifToPublic(pKey); 
		return steem.auth.wifIsValid(pKey,steem.auth.wifToPublic(pKey)) && steem.auth.isWif(pKey);
	}

	login(e){
		var username =this.refs.username_input.value;
		var postingKey =this.refs.postingkey_input.value; 
		if( this.keyIsValid(postingKey) ){
			setCookie('username',username,365);
			setCookie('postingkey',postingKey,365);
		}else{
			console.log('error logging in');
		}
	}

	logout(e){
		setCookie('username','',365);
		setCookie('postingkey','',365);
	}
	</script>
	
</login-form>
