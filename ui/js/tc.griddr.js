if(!tc){ var tc = {}; }

tc.griddr = makeClass();

tc.griddr.prototype.init = function(app,options){
  tc.util.log('tc.griddr.prototype.init');
  this.grid = {};
  this.view = null;
}
  
tc.griddr.prototype.update = function(map){
  tc.util.log('tc.griddr.prototype.update');
  var bounds, zoom, gridbase, gridcenter;
  center = map.getCenter();
  bounds = map.getBounds();
  zoom = map.getZoom();
  gridbase = 10;
  
  //console.log(bounds);
  //console.log(bounds.getNorthEast().lat());
  //console.log(bounds.getNorthEast().lng());
  //console.log(bounds.getSouthWest().lat());
  //console.log(bounds.getSouthWest().lng());
  //console.log(center);
  //console.log(rounded_lat+", "+rounded_lng);
  //console.log(bounds.getNorthEast().lat() - bounds.getSouthWest().lat())
  //console.log(bounds.getNorthEast().lng() - bounds.getSouthWest().lng())
  //console.log(zoom);
  
  gridcenter = new google.maps.LatLng(Math.round(center.lat()/gridbase)*gridbase,Math.round(center.lng()/gridbase)*gridbase);
  this.grid.center = gridcenter;
  
  app.fire('griddr:grid_updated',this.grid);
  
}

tc.griddr.prototype.getView = function(){
  tc.util.log('tc.griddr.prototype.getView');
  if(!this.view){
    this.view = new tc.griddr.view(app.map.instance);
  }
  return this.view;
}
