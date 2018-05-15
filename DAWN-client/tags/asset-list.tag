<asset-list>

<h3>Asset list</h3>

<table class="primary">
	<thead>
		<tr>
			<th>Title</th>
			<th>Author</th>
			<th>Owner</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		<tr each={asset in assets}>
			<td> {asset.title} </td>
			<td> {asset.author} </td>
			<td> {asset.owner} </td>
			<td><a href="#">Actions</a></td>
		</tr>

	</tbody>
</table>

this.assets = [
			{title: 'First asset',author: 'tiago',owner: 'tiagotest'},
			{title: 'Second asset',author: 'tiagouser',owner: 'tiagouser'},
			{title: 'Third asset',author: 'tiago',owner: 'tiagouser'}
]

</asset-list>
