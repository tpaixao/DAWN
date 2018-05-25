<login-button>

<a id="loginButton" class="button"> { this.label } </a>

<script>
	//code
	this.label = 'not set';

	this.on('mount',function(){
		this.label = "Login";
		this.update();
	});
</script>

</login-button>
