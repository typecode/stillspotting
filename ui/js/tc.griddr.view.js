if(!tc){ var tc = {}; }

tc.griddr.view = makeClass();
//tc.griddr.view.prototype = new tc.viz.canvas();
tc.griddr.view.prototype = pv.extend(google.maps.OverlayView);

tc.griddr.view.prototype.init = function(map){
  tc.util.log('tc.griddr.view.prototype.initialize');
  this.map = map;
  this.map_overlays = [];
  this.setMap(this.map);
  this.dom = app.Y.Node.create("<div class='canvas'></div>");
  this.canvas = this.dom._node;
  this.setup_events();
}

tc.griddr.view.prototype.onAdd = function(){
  tc.util.log('tc.griddr.view.prototype.onAdd');
  //this.getPanes().mapPane.appendChild(this.canvas);
  this.getPanes().overlayLayer.appendChild(this.canvas);
}

tc.griddr.view.prototype.setup_events = function(){
  tc.util.log('tc.griddr.view.prototype.setup_events');
  var _me;
  _me = this;
  app.on('griddr:grid_updated',function(d){
    _me.draw(d);
  })
}
  
tc.griddr.view.prototype.draw = function(d){
  tc.util.log('tc.griddr.view.prototype.draw');
  var c, m, p, x, y, i, r;
  c = this.canvas;
  m = app.map;
  p = this.getProjection();
  if(!p){ return; }
  if(!d){ return; }
  
  x = {};
  y = {};
  
  if(d.center){
    xyobj = p.fromLatLngToDivPixel(d.center);
    center_x = xyobj.x;
    x.min = center_x - 10;
    x.max = center_x + 10;
    center_y = xyobj.y;
    y.min = center_y - 10;
    y.max = center_y + 10;
  }
  
  for(i in this.map_overlays){
    this.map_overlays[i].setMap(null);
  }
  this.map_overlays = [];
  
  if(d.units){
    for(i = 0; i < d.units.length; i++){
      r = new google.maps.Rectangle({
        bounds:d.units[i]
      });
      //r.setMap(m.instance);
      this.map_overlays.push(r);
    }
  }
  
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

tc.griddr.view.prototype.replot = function(d){
  var p, c, center_x, center_y;
  p = this.getProjection();
  if(!p){ return; }
  c = this.canvas;
  
}