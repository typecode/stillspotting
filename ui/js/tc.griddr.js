if(!tc){ var tc = {}; }

tc.griddr = makeClass();

tc.griddr.prototype.init = function(app,options){
  tc.util.log('tc.griddr.prototype.init');
  this.grid = {};
  this.view = null;
}
  
tc.griddr.prototype.update = function(map){
  tc.util.log('tc.griddr.prototype.update');
  var bounds, zoom, gridbase, gridcenter, i, j;
  center = map.getCenter();
  bounds = map.getBounds();
  zoom = map.getZoom();
  gridbase = 10;
  
  
  gridcenter = new google.maps.LatLng(
    Math.round(center.lat()/gridbase)*gridbase,
    Math.round(center.lng()/gridbase)*gridbase
  );
  this.grid.center = gridcenter;
  this.grid.units = [];
  for(i = -3; i < 3; i++){
    for(j = -3; j < 3; j++){
      this.grid.units.push(new google.maps.LatLngBounds(
          new google.maps.LatLng(
            gridcenter.lat()-(i*gridbase)-gridbase,
            gridcenter.lng()-(j*gridbase)-gridbase
          ),
          new google.maps.LatLng(
            gridcenter.lat()-(i*gridbase),
            gridcenter.lng()-(j*gridbase)
          )
        )
      );
    }
  }
  
  app.fire('griddr:grid_updated',this.grid);
  
}

tc.griddr.prototype.getView = function(){
  tc.util.log('tc.griddr.prototype.getView');
  if(!this.view){
    this.view = new tc.griddr.view(app.map.instance);
  }
  return this.view;
}
