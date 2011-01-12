if(!tc){ var tc = {}; }

tc.api.results = makeClass();

tc.api.results.prototype.markup = "<div class='api-results'></div>";

tc.api.results.prototype.init = function(app,options){
  tc.util.log('tc.api.results.prototype.init');
  this.dom = app.Y.Node.create(this.markup);
  app.dom.append(this.dom);
  this.setup_events();
}

tc.api.results.prototype.setup_events = function(){
  tc.util.log('tc.api.results.prototype.setup_events');
  var _me;
  _me = this;
  app.on('api-loader:api-query-started', function(){
    _me.dom._node.innerHTML = "<p>Loading...</p>";
  });
  app.on('api-loader:api-data-success', function(data){
    _me.dom._node.innerHTML = "<pre>"+app.Y.JSON.stringify(data,null,'&nbsp;&nbsp;')+"</pre>";
  });
}

