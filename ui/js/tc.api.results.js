if(!tc){ var tc = {}; }

tc.api.results = makeClass();

tc.api.results.prototype.markup = "<div class='api-results'></div>";

tc.api.results.prototype.init = function(app,options){
  tc.util.log('tc.api.results.prototype.init');
  this.dom = app.Y.Node.create(this.markup);
  app.dom.append(this.dom);
}