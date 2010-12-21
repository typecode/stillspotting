if(!tc){ var tc = {}; }

function Canvas(map){
  this.map = map;
  this.setMap(this.map);
  this.initialize();
}

tc.viz = function(options){
  
  _me = this;
  
  _me.map = null;
  _me.overlay = null;
  _me.points = [];
  
  this.initialize = function(){
    tc.util.log('viz.initialize');
    
    Canvas.prototype = pv.extend(google.maps.OverlayView);
    
    Canvas.prototype.initialize = function(map) {
      this.canvas = document.createElement("div");
      this.canvas.setAttribute("class", "canvas");
    };
    
    Canvas.prototype.onAdd = function(){
      this.getPanes().mapPane.appendChild(this.canvas);
    }
    
    Canvas.prototype.draw = function(){
      tc.util.log('Canvas.prototype.draw');
      var c, m, r, projection, points, x, y, pixels;
      if(!_me.points){ return; }
      c = this.canvas;
      m = this.map;
      r = 10;
      projection = this.getProjection();
      
      pixels = _me.points.map(function(d) {
        var xyobj;
        xyobj = projection.fromLatLngToContainerPixel(new google.maps.LatLng(d.lat, d.lng));
        return {x:xyobj.x,y:xyobj.y};
      });
      
      function getx(p) p.x; function gety(p) p.y;
      x = { min: pv.min(pixels, getx) - r, max: pv.max(pixels, getx) + r };
      y = { min: pv.min(pixels, gety) - r, max: pv.max(pixels, gety) + r };
      
      c.style.width = (x.max - x.min) + "px";
      c.style.height = (y.max - y.min) + "px";
      c.style.left = x.min + "px";
      c.style.top = y.min + "px";
      
      new pv.Panel()
        .canvas(this.canvas)
        .left(-x.min)
        .top(-y.min)
          .data(pixels)
            .add(pv.Dot)
              .lineWidth(0.5)
              .strokeStyle('rgba(217, 0, 0, .8)')
              .fillStyle('rgba(217, 0, 0, .5)')
              .left(function() pixels[this.parent.index].x)
              .top(function() pixels[this.parent.index].y)
              .size(r)
                .root.render();
    }
    
    _me.map = new google.maps.Map(document.getElementById("map"),{
      zoom: 3,
      center: new google.maps.LatLng(38, -97),
      mapTypeId: google.maps.MapTypeId.TERRAIN
    });
    _me.overlay = new Canvas(_me.map);
    
    google.maps.event.addListener(_me.map, 'idle', function() {
      //_me.overlay.draw();
    });
    
    return _me;
  }
  
  this.renderComments = function(comments){
    var i, loc;
    for(i in comments){
      loc = comments[i].latlng.response.results[0].geometry.location;
      _me.points.push(loc);
    }
    _me.overlay.draw();
  }
  
  return this.initialize();
}