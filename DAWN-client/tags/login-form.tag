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
		//console.log(steem.auth.isWif(pKey));
		//console.log(steem.auth.wifToPublic(pKey));
		//console.log(pKey);
		//console.log(steem.auth.wifIsValid(pKey,steem.auth.wifToPublic(pKey)));
		//This always returns true
		//get pubkey from blockchain?
		//var pubKey =steem.auth.wifToPublic(pKey); 
		var pubKey; 
		steem.api.getAccounts([username], function(err,result){
			console.log(err,result);
			this.pubKey = result[0]['posting']['key_auths'][0][0];
			//console.log(this.pubKey);
			//return pubKey;
		});
		console.log(pubKey);
		return steem.auth.wifIsValid(pKey,pubKey) && steem.auth.isWif(pKey);
	}

	login(e){
		var username =this.refs.username_input.value;
		var postingKey =this.refs.postingkey_input.value; 
		/*steem.api.getAccounts([username], function(err, result) {*/
  /*console.log(err, result);*/
	/*});*/
		if( this.keyIsValid(username,postingKey) ){
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
