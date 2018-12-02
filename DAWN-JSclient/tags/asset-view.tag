<asset-view>

<div class="card flex-row flex-wrap">
	<div class="card-header border-0">
		<img src="{ asset.picture }" alt="">
	</div>
	<div class="card-block px-2">
		<h4 class="card-title">{ asset.title }</h4>
		<h5 class="card-subtitle text-muted">{ asset.author }</h5>
		<p class="card-text">{ asset.description }</p>
		<a href="#" class="btn btn-primary">Offer</a>
	</div>
	<div class="w-100">stuff</div>
	<div class="card-footer w-100 text-muted">
		footer
	</div>
</div> 

<script>
	this.on('mount',function(){ 
			console.log('asset-view');
			/*asset = JSON.parse( opts.asset );*/
			asset =  opts.asset;
			this.update()
			console.log(asset);
			});
</script>

</asset-view>
