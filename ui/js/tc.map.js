if(!tc){ var tc = {}; }

tc.gmap = makeClass();

tc.gmap.prototype.init = function(app,options){
  tc.util.log('tc.gmap.prototype.initialize');
  
  this.dom = app.Y.Node.create('<div id="map"></div>');
  app.dom.append(this.dom);
  
  this.instance = new google.maps.Map(document.getElementById("map"),{
    zoom: 4,
    center: new google.maps.LatLng(38, -97),
    scrollwheel:false,
    mapTypeControlOptions:{
      mapTypeIds: []
    }
  });
  this.instance.mapTypes.set('TYPE/CODE', tc.gmap.styledMapTypes.base);
  this.instance.setMapTypeId('TYPE/CODE');
  this.setup_events();
}

tc.gmap.prototype.setup_events = function(){
  tc.util.log('tc.gmap.prototype.initialize');
  var _me;
  _me = this;
  google.maps.event.addListener(this.instance, 'mousemove', function(event){
    app.infopane.update('MouseGeo',event.latLng.toString());
    app.infopane.update('MousePos',event.pixel.toString());
  });
  
  google.maps.event.addListener(this.instance, 'bounds_changed', function(){
    var bounds;
    bounds = _me.instance.getBounds();
    app.infopane.update('Bounds',bounds.toString());
    app.griddr.update(_me.instance);
  });
  
  google.maps.event.addListener(this.instance, 'zoom_changed', function(){
    app.infopane.update('Zoom',_me.instance.getZoom());
    //app.fire('map:zoom_changed');
    if(app.gridmanager){
      app.gridmanager.clear_units();
    }
  });
  
  app.infopane.update('Zoom',this.instance.getZoom());
}