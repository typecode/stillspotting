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
  
  gridsize = null;
  switch(zoom){
    case 0:
      gridsize = 360 / 10;
      break;
    case 1:
      gridsize = 360 / 10;
      break;
    case 2:
      gridsize = 360 / 10;
      break;
    case 3:
      gridsize = 222.36328125 / 10;
      break;
    case 4:
      gridsize = 111.18164062500006 / 10;
      break;
    case 5:
      gridsize = 55.5908203125 / 10;
      break;
    case 6:
      gridsize = 27.79541015625 / 10;
      break;
    case 7:
      gridsize = 13.897705078125 / 10;
      break;
    case 8:
      gridsize = 6.9488525390625 / 10;
      break;
    case 9:
      gridsize = 3.47442626953125 / 10;
      break;
    case 10:
      gridsize = 1.737213134765625 / 10;
      break;
    case 11:
      gridsize = 0.8686065673828125 / 10;
      break;
    case 12:
      gridsize = 0.43430328369140625 / 10;
      break;
    case 13:
      gridsize = 0.21715164184570312 / 10;
      break;
    case 14:
      gridsize = 0.10857582092285156 / 10;
      break;
    case 15:
      gridsize = 0.05428791046142578 / 10;
      break;
    case 16:
      gridsize = 0.02714395523071289 / 10;
      break;
    case 17:
      gridsize = 0.013571977615356445 / 10;
      break;
    case 18:
      gridsize = 0.006785988807678223 / 10;
      break;
    case 19:
      gridsize = 0.0033929944038391113 / 10;
      break;
    case 20:
      gridsize = 0.0016964972019195557 / 10;
      break;
  }
  
  if(gridsize > 1){
    gridsize = Math.round(gridsize);
  }

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
  dim = {}
  dim.width = null;
  if(zoom <= 3){
    if(disp_sw.lng() > 0 && disp_ne.lng() > 0){
      if(disp_sw.lng() > disp_ne.lng()){
        dim.width = 180 + (180 - disp_sw.lng()) + disp_ne.lng();
      } else {
        dim.width = 180 + (180 - disp_ne.lng()) + disp_sw.lng();
      }
    } else if(disp_sw.lng() < 0 && disp_ne.lng() < 0){
      if(disp_sw.lng() < disp_ne.lng()){
        dim.width = -180 + (-180 - disp_sw.lng()) + disp_ne.lng();
      } else {
        dim.width = -180 + (-180 - disp_ne.lng()) + disp_sw.lng();
      }
    } else if((disp_sw.lng() < 0 && disp_ne.lng() > 0) ||
              (disp_sw.lng() > 0 && disp_ne.lng() < 0)){
                if(disp_sw.lng() < disp_ne.lng()){
                  dim.width = disp_sw.lng() - disp_ne.lng();
                } else {
                  dim.width = (180 - disp_sw.lng()) + (180 + disp_ne.lng());
                }
              }
  }
  if(!dim.width){
    dim.width = disp_sw.lng()-disp_ne.lng();
  }
  dim.height = disp_sw.lat()-disp_ne.lat();
  
  
  if(dim.width < 0){ dim.width *= -1; }
  if(dim.height < 0){ dim.height *= -1; }
  app.infopane.update('Dimensions', dim.height + ' x ' + dim.width)
  
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
  this.grid.unit_ids = [];
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
      this.grid.unit_ids.push(
        this.grid.zoom+'_'+this.grid.units[this.grid.units.length-1].toUrlValue()
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
