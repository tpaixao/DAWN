riot.tag2('asset-list', '<h3>Asset list</h3> <table class="primary"> <thead> <tr> <th>Title</th> <th>Author</th> <th>Owner</th> <th>Actions</th> </tr> </thead> <tbody> <tr each="{asset in assets}"> <td> {asset.title} </td> <td> {asset.author} </td> <td> {asset.owner} </td> <td><a href="#">Actions</a></td> </tr> </tbody> </table>', '', '', function(opts) {

this.assets = [
			{title: 'First asset',author: 'tiago',owner: 'tiagotest'},
			{title: 'Second asset',author: 'tiagouser',owner: 'tiagouser'},
			{title: 'Third asset',author: 'tiago',owner: 'tiagouser'}
]

});

riot.tag2('login-form', '<div id="login_form" class=""> <article class="card"> <header> <h2>Login</h2> <fieldset class="flex two"> <label> <input id="username_input" type="username" placeholder="STEEM username"></label> <label><input id="postingkey_input" type="password" placeholder="Private Posting Key"></label> </fieldset> <button id="login_button" class="success">Login</button> </header> </article> </div>', '', '', function(opts) {
});

riot.tag2('sidemenu', '<div style="overflow: hidden;height: 50px;"></div> <div> <span class="stack pseudo button icon-picture">My Assets</span> <span class="stack pseudo button icon-puzzle">Search Assets</span> <span class="stack pseudo button icon-help-circled">Register Asset</span> </div>', '', '', function(opts) {
});
