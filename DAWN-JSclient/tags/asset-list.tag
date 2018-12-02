<asset-list>

<div class="row">
	<div class="col-md-3" each={ asset in assets } data={ this }  >
		<!-- <div class="card m-sm-4" style="width: 18rem;"> -->
		<div class="card m-sm-4 h-100" >
			<!-- <img class="card-img-top" src="https://via.placeholder.com/100px80/" alt="Card image cap"> -->
			<img class="card-img" src="https://via.placeholder.com/100px80/" alt="Card image cap"> 
			<div class="card-body d-flex flex-column align-items-start">
			<div class="card-img-overlay" >
				<h4 class="card-title">{ asset.title	}</h4>
				<h5 class="card-subtitle text-muted">{ asset.author.toLowerCase() }</h5>
			</div>
				<p class="card-text">{ asset.description.substring(0,100) + '...'	}</p>
				<div class="flex-row align-items-end mt-auto">
					<a href="#" class="btn btn-primary ">Details</a>
					<!-- <a href="#" class="btn btn-primary">Buy</a> -->
				</div>
			</div>
		</div>
	</div>
</div>

<script>

self = this;


this.on('mount',() => fetch('/generated.json')
		.then(function(response){
			self.data = response.json()
			/*console.log(self.data);*/
			/*self.update()*/
			return self.data;
		})
		.then(function (myjson){
			console.log(myjson);
			self.assets = myjson;
			console.log(self.assets[0]);
			self.update();
			/*riot.update()*/
		})
);

</script>

</asset-list>
