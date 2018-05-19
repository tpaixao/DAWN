<login-form >
	<div id="login_form" class="" style="width: 100%">
		<article class="card">
			<header>
				<h2>Login</h2>
				<fieldset class="flex two">
					<label> <input ref="username_input" type="username" placeholder="STEEM username"></label>
					<label><input ref="postingkey_input" type="password" placeholder="Private Posting Key"></label>
				</fieldset>	
				<a ref="login_button" class="button sucess" onclick={ this.login }>Login</a>
			</header>
		</article>

	</div>

	//code
	<script>

	this.on('mount',function() {
		console.log("login-form mounted")
	});

	keyIsValid(username, pKey){
		//get pubkey from blockchain?
		//var pubKey =steem.auth.wifToPublic(pKey); 
		var pubKey; 
		console.log(err,result);
		this.pubKey = result[0]['posting']['key_auths'][0][0];
		console.log(pubKey);
		//steem.auth.wifIsValid(pKey,pubKey) && steem.auth.isWif(pKey);

		if( steem.auth.wifIsValid(pKey,pubKey) && steem.auth.isWif(pKey)){
			//login is valid
			setCookie('username',username,365);
			setCookie('postingkey',postingKey,365);
		}else{
			console.log('error logging in');
		}
 }

	login(e){
		var username =this.refs.username_input.value;
		var postingKey =this.refs.postingkey_input.value; 
		/*steem.api.getAccounts([username], function(err, result) {*/
  /*console.log(err, result);*/
	/*});*/
		steem.api.getAccounts([username], keyIsValid(err,result));
	}

	logout(e){
		setCookie('username','',365);
		setCookie('postingkey','',365);
	}

	</script>
	
</login-form>
