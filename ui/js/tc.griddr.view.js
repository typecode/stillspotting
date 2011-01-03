if(!tc){ var tc = {}; }

tc.griddr.view = makeClass();
//tc.griddr.view.prototype = new tc.viz.canvas();
tc.griddr.view.prototype = pv.extend(google.maps.OverlayView);

tc.griddr.view.prototype.init = function(map){
  tc.util.log('tc.griddr.view.prototype.initialize');
  this.map = map;
  this.setMap(this.map);
  this.dom = app.Y.Node.create("<div class='canvas'></div>");
  this.canvas = this.dom._node;
  this.setup_events();
}

tc.griddr.view.prototype.onAdd = function(){
  tc.util.log('tc.griddr.view.prototype.onAdd');
  //app.Y.one('#map').append(this.canvas);
  this.getPanes().mapPane.appendChild(this.canvas);
  //this.getPanes().overlayLayer.appendChild(this.canvas);
}

tc.griddr.view.prototype.setup_events = function(){
  tc.util.log('tc.griddr.view.prototype.setup_events');
  var _me;
  _me = this;
  app.on('griddr:grid_updated',function(d){
    //_me.draw(d);
    //_me.replot(d);
  })
}
  
tc.griddr.view.prototype.draw = function(d){
  tc.util.log('tc.griddr.view.prototype.draw');
  //if(!d){ return; }
  var c, m, p;
  c = this.canvas;
  m = app.map;
  p = this.getProjection();
  if(!p){ return; }
  
  c.style.border = '1px solid red';
  c.style.width = app.dom._node.offsetWidth+"px";
  c.style.height = app.dom._node.offsetHeight+"px";
  //c.style.left = (this.dom.getX()*-1.0)+'px';
  //c.style.top = (this.dom.getY()*-1.0)+'px';
  
  if(!d){ return; }
  this.replot(d);
}

tc.griddr.view.prototype.replot = function(d){
  var p, c, center_x, center_y;
  p = this.getProjection();
  if(!p){ return; }
  c = this.canvas;
  xyobj = p.fromLatLngToDivPixel(d.center);
  center_x = xyobj.x;
  center_y = xyobj.y;
  
  new pv.Panel()
    .canvas(c)
    .left(0)
    .top(0)
      .add(pv.Panel)
        .add(pv.Dot)
          .lineWidth(0.0)
          .def("fillStyle", 'rgba(217, 0, 0, .5)')
          .left(center_x)
          .top(center_y)
          .size(10)
        .root.render();
}