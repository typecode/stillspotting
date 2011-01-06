if(!tc){ var tc = {}; }

tc.geoitem.view = makeClass();
tc.geoitem.view.prototype = pv.extend(google.maps.OverlayView);

tc.geoitem.view.prototype.init = function(map){
  tc.util.log('tc.geoitem.view.prototype.initialize');
  this.map = map;
  this.setMap(this.map);
  this.dom = app.Y.Node.create("<div class='canvas'></div>");
  this.canvas = this.dom._node;
  this.canvas.style.zIndex = '100';
  
  this.current_gridunits = [];
  
  this.setup_events();
}

tc.geoitem.view.prototype.onAdd = function(){
  tc.util.log('tc.geoitem.view.prototype.onAdd');
  this.getPanes().overlayLayer.appendChild(this.canvas); 
}

tc.geoitem.view.prototype.setup_events = function(){
  tc.util.log('tc.geoitem.view.prototype.setup_events');
  var _me;
  _me = this;
  app.on('gridloader:gridunit_loaded',function(d){
    tc.util.log('tc.geoitem.view.prototype.setup_events(gridloader:gridunit_loaded)');
    //if(!_me.current_gridunits[d.grid_id]){
    //  _me.current_gridunits[d.grid_id] = d.gridunit_data;
    //  _me.current_gridunits[d.grid_id].rendered = false;
    //}
    _me.current_gridunits.push(d.gridunit_data);
    _me.draw();
  });
}

tc.geoitem.view.prototype.draw = function(){
  tc.util.log('tc.geoitem.view.prototype.draw');
  var i, m, c, mbc, mybounds;
  u = this.current_gridunits;
  m = this.map;
  c = this.canvas;
  
  console.log(this.current_gridunits);
  
  function min_lat(p){
    console.log('min_lat');
    console.log(p);
  };
  function max_lat(p){
    console.log('max_lat');
    console.log(p);
  };
  function min_lng(p){
    console.log('min_lng');
    console.log(p);
  };
  function max_lng(p){
    console.log('max_lng');
    console.log(p);
  };
  var x = { min: pv.min(u, min_lng), max: pv.max(u, max_lng) };
  var y = { min: pv.min(u, max_lat), max: pv.max(u, max_lat) };

  
  return;
  
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