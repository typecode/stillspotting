if(!tc){ var tc = {}; }

tc.griddr = makeClass();

tc.griddr.prototype.init = function(app,options){
  tc.util.log('tc.griddr.prototype.init');
  this.grid = {};
  this.last_center = null;
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
  
  if(this.last_center){
    if(this.last_center.equals(gridcenter)){ return; }
  }
  
  disp_ne = bounds.getNorthEast();
  disp_sw = bounds.getSouthWest();
  dim = {
    width:disp_sw.lng()-disp_ne.lng(),
    height:disp_sw.lat()-disp_ne.lat()
  }
  if(dim.width < 0){ dim.width *= -1; }
  if(dim.height < 0){ dim.height *= -1; }
  app.infopane.update('Dimensions', dim.height + ' x ' + dim.width)
  
  grid_dim = {
    width:Math.ceil(dim.width/gridbase),
    height:Math.ceil(dim.height/gridbase)
  }
  if(grid_dim.width%2){ grid_dim.width += 1; }
  if(grid_dim.height%2){ grid_dim.height += 1; }
  
  app.infopane.update('GridDimensions', grid_dim.height + ' x ' + grid_dim.width)
  
  console.log(grid_dim);
  
  this.last_center = gridcenter;
  this.grid.center = gridcenter;
  this.grid.units = [];
  for(i = -grid_dim.height/2; i < grid_dim.height/2; i++){
    for(j = -grid_dim.width/2; j < grid_dim.width/2; j++){
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
