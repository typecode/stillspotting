if(!tc){ var tc = {}; }

tc.viz.canvas = makeClass();
tc.viz.canvas.prototype = pv.extend(google.maps.OverlayView);

tc.viz.canvas.prototype.init = function(map){
  tc.util.log('tc.viz.canvas.prototype.init');
  this.map = map;
  this.setMap(this.map);
  this.canvas = document.createElement("div");
  this.canvas.setAttribute("class", "canvas");
}

tc.viz.canvas.prototype.onAdd = function(){
  tc.util.log('tc.viz.canvas.prototype.onAdd');
  this.getPanes().mapPane.appendChild(this.canvas);
}
    
tc.viz.canvas.prototype.draw = function(){
  tc.util.log('tc.viz.canvas.prototype.draw');
  // var c, m, p, r, points, x, y, pixels;
  //   if(!_me.points || !_me.points.length){ return; }
  //   c = this.canvas;
  //   m = this.map;
  //   p = this.getProjection();
  //   r = 10;
  //   pixels = [];
  //   
  //   pixels = _me.points.map(function(d) {
  //     var xyobj;
  //     //xyobj = p.fromLatLngToContainerPixel(new google.maps.LatLng(d.lat, d.lng));
  //     xyobj = p.fromLatLngToDivPixel(new google.maps.LatLng(d.lat, d.lng));
  //     return {x:xyobj.x,y:xyobj.y};
  //   });
  //   
  //   function getx(p) p.x; function gety(p) p.y;
  //   x = { min: pv.min(pixels, getx) - r, max: pv.max(pixels, getx) + r };
  //   y = { min: pv.min(pixels, gety) - r, max: pv.max(pixels, gety) + r };
  //   
  //   c.style.width = (x.max - x.min) + "px";
  //   c.style.height = (y.max - y.min) + "px";
  //   c.style.left = x.min + "px";
  //   c.style.top = y.min + "px";
  //   
  //   new pv.Panel()
  //     .canvas(this.canvas)
  //     .left(-x.min)
  //     .top(-y.min)
  //       .add(pv.Panel)
  //         .data(pixels)
  //       .add(pv.Dot)
  //         .lineWidth(0.0)
  //         .def("fillStyle", 'rgba(217, 0, 0, .5)')
  //         .left(function() pixels[this.parent.index].x)
  //         .top(function() pixels[this.parent.index].y)
  //         .event("mouseover", function(){
  //           console.log(this);
  //           console.log('over');
  //           this.fillStyle('rgba(0, 217, 0, .5)');
  //         })
  //         .event("mouseout", function(){
  //           console.log('out');
  //           this.fillStyle(undefined);
  //         })
  //         .size(r)
  //       .root.render();
}