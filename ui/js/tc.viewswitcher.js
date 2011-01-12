if(!tc){ var tc = {}; }

tc.viewswitcher = makeClass();
tc.viewswitcher.prototype = pv.extend(google.maps.OverlayView);

tc.viewswitcher.prototype.init = function(map){
  tc.util.log('tc.viewswitcher.prototype.init');
  this.dom = app.Y.Node.create("<div>\
    <br/><br/><br/><br/>\
    <a href='#api'>api</a>\
    <a href='#map'>map</a>\
  </div>");
  app.dom.append(this.dom);
}