if(!tc){ var tc = {}; }

tc.griddr.gridunit = makeClass();
tc.griddr.gridunit.prototype = pv.extend(google.maps.OverlayView);

tc.griddr.gridunit.prototype.init = function(map,data){
  tc.util.log('tc.griddr.gridunit.prototype.initialize');
  if(!data || !map){return false;}
  this.map = map;
  this.setMap(this.map);
  this.bounds = null;
  this.dom = app.Y.Node.create("<div class='canvas'></div>");
  this.canvas = this.dom._node;
  this.hidden = false;
  this.rendered = false;
  this.points = null;
  
  this.update(data);
}


tc.griddr.gridunit.prototype.add = function(){
  tc.util.log('tc.griddr.gridunit.prototype.add');
  this.onAdd();
}

tc.griddr.gridunit.prototype.clear_from_map = function(){
  tc.util.log('tc.griddr.gridunit.prototype.clear_from_map');
  this.setMap(null);
  this.dom.destroy();
  //delete this;
}

tc.griddr.gridunit.prototype.update = function(data){
  tc.util.log('tc.griddr.gridunit.prototype.update');
  this.rendered = false;
  this.data = data;
  this.id = this.data.unit_id;
  this.points = null;
  this.draw();
}

tc.griddr.gridunit.prototype.onAdd = function(){
  tc.util.log('tc.griddr.view.prototype.onAdd');
  this.getPanes().overlayLayer.appendChild(this.canvas);
}

tc.griddr.gridunit.prototype.draw = function(data){
  tc.util.log('tc.griddr.gridunit.prototype.draw');
  var _me, m,c, p, x, y;
  
  if(this.rendered){ return; }
  if(this.hidden){ return; }
  if(!this.data){ return; }
  
  _me = this;
  m = this.map;
  z = this.map.getZoom();
  if(z != this.data.unit_id.split(',')[0]){
    this.clear_from_map();
    return;
  }
  c = this.canvas;
  m = this.map;
  p = this.getProjection();
  if(!p){ return; }
  
  
  ne_obj = p.fromLatLngToDivPixel(new google.maps.LatLng(
    this.data.gridunit_data.bounds[0],
    this.data.gridunit_data.bounds[1]
  ));
  sw_obj = p.fromLatLngToDivPixel(new google.maps.LatLng(
    this.data.gridunit_data.bounds[2],
    this.data.gridunit_data.bounds[3]
  ));
  
  if(!this.points){
    this.points = this.data.gridunit_data.points.map(function(d) {
      return p.fromLatLngToDivPixel(new google.maps.LatLng(d.loc[0], d.loc[1]));
    });
  }
  
  x = {min:ne_obj.x > sw_obj.x ? sw_obj.x : ne_obj.x, max:ne_obj.x > sw_obj.x ? ne_obj.x : sw_obj.x};
  y = {min:ne_obj.y > sw_obj.y ? sw_obj.y : ne_obj.y, max:ne_obj.y > sw_obj.y ? ne_obj.y : sw_obj.y};
  
  //c.style.border = "1px solid green";
  c.style.width = (x.max - x.min) + "px";
  c.style.height = (y.max - y.min) + "px";
  c.style.left = x.min + "px";
  c.style.top = y.min + 'px';
  
  new pv.Panel()
    .canvas(c)
      .left(-x.min)
      .top(-y.min)
        .add(pv.Panel)
          .data(this.points)
            .add(pv.Dot)
              .left(function(){
                return _me.points[this.parent.index].x;
              })
              .top(function(){
                return _me.points[this.parent.index].y;
              })
              .lineWidth(0)
              .fillStyle('rgba(255,0,0,0.5)')
              .size(1)
          .root.render();
  
  this.rendered = true;
}