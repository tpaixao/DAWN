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

	keyIsValid(result){
		//get pubkey from blockchain?
		//var pubKey =steem.auth.wifToPublic(pKey); 
		console.log(result);
		this.pubKey = result[0]['posting']['key_auths'][0][0];
		console.log(this.pubKey);
		//steem.auth.wifIsValid(pKey,pubKey) && steem.auth.isWif(pKey);

		if( steem.auth.wifIsValid(privKey,pubKey) ){
			//login is valid
			setCookie('username',this.username,365);
			setCookie('postingkey',this.privKey,365);
		}else{
			console.log('error logging in');
		}
 }

	login(e){
		var username =this.refs.username_input.value;
		var privKey =this.refs.postingkey_input.value; 

		var validkey = function (result){
			//get pubkey from blockchain?
			//var pubKey =steem.auth.wifToPublic(pKey); 
			console.log(result);
			var pubKey = result[0]['posting']['key_auths'][0][0];
			console.log(pubKey);
			console.log(privKey);
			//steem.auth.wifIsValid(pKey,pubKey) && steem.auth.isWif(pKey);
			var isvalid; 
			try{ isvalid = steem.auth.wifIsValid(privKey, pubKey); }
			catch(e){ isvalid = 'false'; }

			console.log(isvalid);

			if(isvalid==true){
				//login is valid
				setCookie('username',this.username,365);
				setCookie('postingkey',this.privKey,365);
			}else{
				console.log('error logging in');
			}
		}

		steem.api.getAccounts([username], function(err,result) {
			//console.log(err);
			validkey(result);
		});
}

	logout(e){
		setCookie('username','',365);
		setCookie('postingkey','',365);
	}

	</script>
	
</login-form>
