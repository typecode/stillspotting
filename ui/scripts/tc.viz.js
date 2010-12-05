if(!tc){ var tc = {}; }

function Canvas(map){
	this.map = map;
	this.setMap(map);
}

tc.viz = function(options){
  
  _me = this;
  
  this.initialize = function(){
    tc.util.log('viz.initialize');
    
    Canvas.prototype = pv.extend(google.maps.OverlayView);
    
    Canvas.prototype.onAdd = function(){
      this.canvas = document.createElement("div");
      this.canvas.setAttribute("class", "canvas");
      this.getPanes().mapPane.appendChild(this.canvas);
    }
    
    Canvas.prototype.draw = function(){
      var m = this.map;
      var c = this.canvas;
      var r = 20;
      
      var projection = this.getProjection();
      
      this.crimes = [];
      
      var pixels = this.crimes.map(function(d) {
        return projection.fromLatLngToDivPixel(new google.maps.LatLng(d.lat, d.lon));
      });
      
      function x(p) p.x; function y(p) p.y;
      var x = { min: pv.min(pixels, x) - r, max: pv.max(pixels, x) + r };
      var y = { min: pv.min(pixels, y) - r, max: pv.max(pixels, y) + r };
      c.style.width = (x.max - x.min) + "px";
      c.style.height = (y.max - y.min) + "px";
      c.style.left = x.min + "px";
      c.style.top = y.min + "px";
      
      new pv.Panel()
        .canvas(c)
        .left(-x.min)
        .top(-y.min)
        .add(pv.Panel)
    }
    
    var map = new google.maps.Map(document.getElementById("map"),{
      zoom: 3,
      center: new google.maps.LatLng(38, -97),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    var overlay = new Canvas(map);
    
    //var map = new GMap2(document.getElementById("map"));
    //
    
    //
    //map.setCenter(new GLatLng(55, 31), 6);
    //var ui = map.getDefaultUI();
    //ui.maptypes.satellite = false;
    //map.setUI(ui);
    //map.setMapType(G_PHYSICAL_MAP);
    //map.addOverlay(new PVCanvas());
    
    //_me.viz = new pv.Panel();
    //_me.viz
    //  .width(app.Y.one('document').get('winWidth')-200)
    //  .height(app.Y.one('document').get('winHeight'))
    //.root.render();
    //_me.add_baseline();
    return _me;
  }
  
  this.add_baseline = function(){
    _me.viz
      .left(0)
      .top(100)
        .add(pv.Line)
          .data([0,1])
          .top(300)
          .left(function(d){ return d*_me.viz.width(); });
          
    _me.viz
      .left(0)
      .top(0)
        .add(pv.Label)
          .data([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
          .top(320)
          .left(function(d){return 10+d*((_me.viz.width()-20)/24);})
          .textAlign('center')
          .text(function(d){ return d; })
        
    _me.viz.render();
  }
  
  this.addWireItems = function(items){
    tc.util.log('tc.viz.addWireItems');
    
    _me.viz
      .add(pv.Bar)
        .data(items)
        .left(function(d){ 
          var date;
          date = d.updated_date.split('T')[1].split('-')[0].split(':');
          console.log(date);
          d.updated_date.split('T')[1]
          return (_me.viz.width()/24*date[0]) + (_me.viz.width()/1440*date[1])
        })
        .top(50)
        .height(250)
        .width(1)
    
    _me.viz.render();
    
  }
  
  return this.initialize();
}