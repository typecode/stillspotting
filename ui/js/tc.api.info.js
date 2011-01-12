if(!tc){ var tc = {}; }

tc.api.info = makeClass();

tc.api.info.prototype.markup = "<div class='api-info'></div>";

tc.api.info.prototype.init = function(app,options){
  tc.util.log('tc.api.info.prototype.init');
  this.dom = app.Y.Node.create(this.markup);
  app.dom.append(this.dom);
}