if(!tc){ var tc = {}; }

tc.viz = makeClass();

tc.viz.prototype.init = function(app,options){
  tc.util.log('tc.viz.prototype.init');
  //this.overlay = new tc.viz.canvas(app.map.instance);
  this.viz_layers = {};
}

tc.viz.prototype.addLayer = function(name,view){
  tc.util.log('tc.viz.addLayer');
  if(!this.viz_layers[name]){
    this.viz_layers[name] = view;
  }
}



tc.viz.prototype.renderComments = function(){
  tc.util.log('tc.viz.renderComments');
  var i, loc, xy, p;
  p = this.overlay.getProjection();
  for(i in comments){
    loc = comments[i].latlng.response.results[0].geometry.location;
    this.points.push(loc);
  }
  this.overlay.draw(true);
}
