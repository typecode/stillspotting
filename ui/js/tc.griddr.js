if(!tc){ var tc = {}; }

tc.griddr = makeClass();

tc.griddr.prototype.init = function(app,options){
  tc.util.log('tc.griddr.prototype.init');
  this.grid = {};
  this.last_zoom = null;
  this.last_center = null;
  this.view = null;
}
  
tc.griddr.prototype.update = function(map){
  //tc.util.log('tc.griddr.prototype.update');
  var bounds, zoom, gridbase, gridcenter, i, j,
    idealgridwidth, disp_ne, disp_sw, dim, gridsize, grid_dim;
  center = map.getCenter();
  bounds = map.getBounds();
  zoom = map.getZoom();
  app.infopane.update('Center', center.toString());
  
  idealgridwidth = 10;
  gridbase = 10;
  
  this.grid.new_zoom = false;
  if(this.last_zoom){
    if(this.last_zoom !== zoom){
      this.grid.new_zoom = true;
    }
  }
  this.grid.zoom = zoom;
  this.last_zoom = zoom;
  
  disp_ne = bounds.getNorthEast();
  disp_sw = bounds.getSouthWest();
  dim = {
    width:disp_sw.lng()-disp_ne.lng(),
    height:disp_sw.lat()-disp_ne.lat()
  }
  if(dim.width < 0){ dim.width *= -1; }
  if(dim.height < 0){ dim.height *= -1; }
  app.infopane.update('Dimensions', dim.height + ' x ' + dim.width)
  
  gridsize = ((dim.width/idealgridwidth)/gridbase)*gridbase;
  if(gridsize > 1){
    gridsize = Math.round(gridsize);
  }
  
  app.infopane.update('GridSize',gridsize);
  
  this.grid.center = center;
  gridcenter = new google.maps.LatLng(
    Math.round(center.lat()/gridsize)*gridsize,
    Math.round(center.lng()/gridsize)*gridsize
  );
  
  if(this.last_center){
    if(this.last_center.equals(gridcenter)){
      this.grid.new_gridcenter = false;
      return;
    }
  }
  this.grid.new_gridcenter = true;
  this.last_center = gridcenter;
  app.infopane.update('GridCenter', gridcenter.toString());
  
  grid_dim = {
    width:Math.ceil(dim.width/gridsize),
    height:Math.ceil(dim.height/gridsize)
  }
  if(grid_dim.width%2){ grid_dim.width += 1; }
  if(grid_dim.height%2){ grid_dim.height += 1; }
  app.infopane.update('GridDimensions', grid_dim.height + ' x ' + grid_dim.width)
  
  this.grid.gridcenter = gridcenter;
  this.grid.units = [];
  for(i = -grid_dim.height/2; i < grid_dim.height/2; i++){
    for(j = -grid_dim.width/2; j < grid_dim.width/2; j++){
      this.grid.units.push(new google.maps.LatLngBounds(
          new google.maps.LatLng(
            gridcenter.lat()-(i*gridsize)-gridsize,
            gridcenter.lng()-(j*gridsize)-gridsize
          ),
          new google.maps.LatLng(
            gridcenter.lat()-(i*gridsize),
            gridcenter.lng()-(j*gridsize)
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
