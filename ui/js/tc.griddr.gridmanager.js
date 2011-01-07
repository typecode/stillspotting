if(!tc){ var tc = {}; }

tc.griddr.gridmanager = makeClass();

tc.griddr.gridmanager.prototype.init = function(app,options){
  tc.util.log('tc.griddr.gridmanager.prototype.initialize');
  this.setup_events();
  this.gridunits = {};
  
}

tc.griddr.gridmanager.prototype.setup_events = function(){
  tc.util.log('tc.griddr.gridmanager.prototype.setup_events');
  var _me;
  _me = this;
  app.on('gridloader:gridunit_loaded',function(d){
    tc.util.log('tc.griddr.gridmanager.prototype.setup_events(gridloader:gridunit_loaded)');
    _me.handle_gridunit_data(d);
  });
  
  app.on('map:zoom_changed',function(d){
    tc.util.log('tc.griddr.gridmanager.prototype.setup_events(map:zoom_changed)');
    _me.clear_units();
  });

}

tc.griddr.gridmanager.prototype.clear_units = function(data){
  tc.util.log('tc.griddr.gridmanager.prototype.clear_units');
  var i;
  for(i in this.gridunits){
    console.log('removing '+ i);
    this.gridunits[i].clear_from_map();
  }
}

tc.griddr.gridmanager.prototype.handle_gridunit_data = function(data){
  tc.util.log('tc.griddr.gridmanager.prototype.handle_gridunit_data');
  var gridunit;
  if(!this.gridunits[data.unit_id]){
    gridunit = this.create_gridunit(data);
  } else {
    gridunit = this.update_gridunit(data);
  }
  if(gridunit){
    app.fire('griddr.gridmanager:gridunit_updated',gridunit);
  }
}

tc.griddr.gridmanager.prototype.create_gridunit = function(data){
  tc.util.log('tc.griddr.gridmanager.prototype.create_gridunit');
  var unit;
  unit = new tc.griddr.gridunit(app.map.instance,data);
  this.gridunits[data.unit_id] = unit;
  return unit;
}

tc.griddr.gridmanager.prototype.update_gridunit = function(data){
  tc.util.log('tc.griddr.gridmanager.prototype.update_gridunit');
  this.gridunits[data.unit_id].update(data);
  return this.gridunits[data.unit_id];
}