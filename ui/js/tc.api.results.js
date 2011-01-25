if(!tc){ var tc = {}; }

tc.api.results = makeClass();

tc.api.results.prototype.markup = "<div class='api-results'>\
  <div class='hd'></div>\
  <div class='bd'></div>\
  <div class='ft'></div>\
</div>";

tc.api.results.prototype.init = function(app,options){
  tc.util.log('tc.api.results.prototype.init');
  this.dom = app.Y.Node.create(this.markup);
  if(options.width){
    this.dom.addClass(options.width).addClass('column');
  }
  app.Y.one(options.target_element).append(this.dom);
  this.setup_events();
}

tc.api.results.prototype.setup_events = function(){
  tc.util.log('tc.api.results.prototype.setup_events');
  var _me;
  _me = this;
  app.on('api-loader:api-query-started', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p>Loading: <a href='http://"+window.location.host+""+data.url+"'>http://"+window.location.host+""+data.url+"</a></p>");
  });
  app.on('api-loader:api-data-success', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p>Loaded: <a href='http://"+window.location.host+""+data.url+"'>http://"+window.location.host+""+data.url+"</a></p>");
    _me.dom.one('.bd').append("<pre>"+app.Y.JSON.stringify(data.data,null,'  ')+"</pre>");
  });
  app.on('api-loader:api-data-error', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p>Error on: <a href='http://"+window.location.host+""+data.url+"'>http://"+window.location.host+""+data.url+"</a></p>");
    _me.dom.one('.bd').append("<pre>ERROR! PLEASE CHECK QUERY SYNTAX</pre>");
  });
}

