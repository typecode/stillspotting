if(!tc){ var tc = {}; }

tc.griddr.view = makeClass();
tc.griddr.view.prototype = pv.extend(google.maps.OverlayView);

tc.griddr.view.prototype.init = function(map){
  tc.util.log('tc.griddr.view.prototype.initialize');
  this.map = map;
  this.map_overlays = [];
  this.map_overlays_by_key = {};
  this.setMap(this.map);
  this.dom = app.Y.Node.create("<div class='canvas'></div>");
  this.canvas = this.dom._node;
  this.canvas.style.zIndex = '100';
  this.grid_data = null;
  this.setup_events();
}

tc.griddr.view.prototype.onAdd = function(){
  tc.util.log('tc.griddr.view.prototype.onAdd');
  this.getPanes().overlayLayer.appendChild(this.canvas);
}

tc.griddr.view.prototype.setup_events = function(){
  tc.util.log('tc.griddr.view.prototype.setup_events');
  var _me;
  _me = this;
  app.on('griddr:grid_updated',function(d){
    tc.util.log('tc.griddr.view.prototype.setup_events(griddr:grid_updated)');
    _me.grid_data = d;
    _me.draw();
  });
  app.on('gridloader:gridunit_loaded',function(d){
    tc.util.log('tc.griddr.view.prototype.setup_events(gridloader:gridunit_loaded)');
    if(_me.map_overlays_by_key[d.unit_id]){
      _me.map_overlays_by_key[d.unit_id].setOptions({
        fillColor:"#FF0000",
        fillOpacity:0.2
      });
    }
  });
}
  
tc.griddr.view.prototype.draw = function(){
  tc.util.log('tc.griddr.view.prototype.draw');
  var c, m, p, d, x, y, i, r,
    show_grid, show_gridcenter;
  c = this.canvas;
  m = app.map;
  p = this.getProjection();
  d = this.grid_data;
  show_grid = true;
  show_gridcenter = true;
  if(!p){ return; }
  if(!d){ return; }
  
  x = {};
  y = {};
  
  if(d.center){
    //draw center here
  }
  
  if(!d.new_gridcenter){
    return;
  }
  
  if(d.gridcenter){
    xyobj = p.fromLatLngToDivPixel(d.gridcenter);
    center_x = xyobj.x;
    x.min = center_x - 10;
    x.max = center_x + 10;
    center_y = xyobj.y;
    y.min = center_y - 10;
    y.max = center_y + 10;
  }
  
  this.map_overlays_by_key = {};
  if(show_grid){
    if(this.map_overlays.length == d.units.length){
      for(i in this.map_overlays){
        this.map_overlays[i].setBounds(d.units[i]);
        this.map_overlays_by_key[d.unit_ids[i]] = this.map_overlays[i];
      }
    } else {
      for(i in this.map_overlays){
        this.map_overlays[i].setMap(null);
        this.map_overlays_by_key = null;
      }
      this.map_overlays = [];
      this.map_overlays_by_key = [];
      if(d.units){
        for(i = 0; i < d.units.length; i++){
          r = new google.maps.Rectangle({
            bounds:d.units[i],
            strokeWeight:0.5,
            strokeOpacity:0.5,
            fillOpacity:0.0
          });
          r.setMap(m.instance);
          this.map_overlays_by_key[d.unit_ids[i]] = r;
          this.map_overlays.push(r);
        }
      }
    }
  }
  
  if(show_gridcenter){
    c.style.width = (x.max - x.min) + "px";
    c.style.height = (y.max - y.min) + "px";
    c.style.left = x.min + "px";
    c.style.top = y.min + 'px';
  
    new pv.Panel()
      .canvas(c)
      .left(0)
      .top(0)
        .add(pv.Panel)
          .add(pv.Dot)
            .lineWidth(0.0)
            .def("fillStyle", 'rgba(217, 0, 0, .5)')
            .left(center_x - x.min)
            .top(center_y - y.min)
            .size(10)
          .root.render();
  }
  
}