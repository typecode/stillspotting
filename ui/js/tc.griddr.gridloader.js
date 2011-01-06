if(!tc){ var tc = {}; }

tc.griddr.gridloader = makeClass();

tc.griddr.gridloader.prototype.init = function(app,options){
  tc.util.log('tc.griddr.gridloader.prototype.initialize');
  this.grid_data = null;
  this.setup_events();
  this.queue_running = false;
  this.queued_requests = [];
  this.grid_data_fetched_observer = null;
  this.cached_gridunit_data = {};
}

tc.griddr.gridloader.prototype.setup_events = function(){
  tc.util.log('tc.griddr.gridloader.prototype.setup_events');
  var _me;
  _me = this;
  app.on('griddr:grid_updated',function(d){
    //tc.util.log('tc.griddr.gridloader.prototype.setup_events(griddr:grid_updated)');
    _me.grid_data = d;
    _me.update()
  });
}

tc.griddr.gridloader.prototype.update = function(){
  //tc.util.log('tc.griddr.gridloader.prototype.update');
  var d;
  d = this.grid_data;
  if(d.new_zoom){
    this.clear_queue();
  }
  if(d.units){
    for(i = 0; i < d.units.length; i++){
      this.handle_gridunit(d.units[i]);
    }
  }
}

tc.griddr.gridloader.prototype.handle_gridunit = function(grid_unit){
  //tc.util.log('tc.griddr.gridloader.prototype.handle_gridunit');
  var cached_data, grid_id;
  grid_id = this.grid_data.zoom+'_'+grid_unit.toUrlValue();
  cached_data = this.cached_gridunit_data[grid_id];
  if(cached_data){
    this.handle_gridunit_data(grid_id,cached_data);
  } else {
    this.add_request_to_queue(this.generate_request(grid_id,grid_unit));
  }
}

tc.griddr.gridloader.prototype.generate_request = function(grid_id,grid_unit){
  //tc.util.log('tc.griddr.gridloader.prototype.generate_request');
  var ne, sw, url, request;
  ne = grid_unit.getNorthEast().toUrlValue();
  sw = grid_unit.getSouthWest().toUrlValue();
  url = '/geoitem/bounds/'+ne+'/'+sw+'/';
  request = {
    url:url,
    grid_id:grid_id
  }
  return request;
}

tc.griddr.gridloader.prototype.add_request_to_queue = function(request){
  //tc.util.log('tc.griddr.gridloader.prototype.add_request_to_queue');
  this.queued_requests.push(request);
  if(!this.queue_running){
    this.run_queue();
  }
}

tc.griddr.gridloader.prototype.run_queue = function(){
  tc.util.log('tc.griddr.gridloader.prototype.run_queue');
  var _me;
  _me = this;
  this.queue_running = true;
  app.infopane.update('nItemsGridloaderQueue',this.queued_requests.length);
  this.request_gridunit_data(this.queued_requests.shift());
  this.grid_data_fetched_observer = app.Y.on('gridloader:griddata_fetched',function(){
    _me.griddata_fetched_handler();
  });
}

tc.griddr.gridloader.prototype.clear_queue = function(){
  //tc.util.log('tc.griddr.gridloader.prototype.clear_queue');
  this.queued_requests = [];
  app.infopane.update('nItemsGridloaderQueue',this.queued_requests.length);
  this.stop_queue();
}

tc.griddr.gridloader.prototype.griddata_fetched_handler = function(){
  //tc.util.log('tc.griddr.gridloader.prototype.griddata_fetched_handler');
  app.infopane.update('nItemsGridloaderQueue',this.queued_requests.length);
  if(this.queued_requests.length){
    this.request_gridunit_data(this.queued_requests.shift());
  } else {
    this.stop_queue();
  }
}

tc.griddr.gridloader.prototype.stop_queue = function(){
  tc.util.log('tc.griddr.gridloader.prototype.stop_queue');
  this.queue_running = false;
  app.infopane.update('nItemsGridloaderQueue',this.queued_requests.length);
  if(this.grid_data_fetched_observer){
    this.grid_data_fetched_observer.detach();
  }
}

tc.griddr.gridloader.prototype.request_gridunit_data = function(request){
  //tc.util.log('tc.griddr.gridloader.prototype.generate_request');
  var _me, cached_data;
  _me = this;
  cached_data = this.cached_gridunit_data[request.grid_id];
  if(cached_data){
    this.handle_gridunit_data(request.grid_id,cached_data);
    app.Y.fire('gridloader:griddata_fetched');
    return;
  }
  app.Y.io(request.url,
    {
      on:{
        success:function(transactionId, response, arguments){
          var json;
          try{
            json = app.Y.JSON.parse(response.responseText);
          } catch(e){ tc.util.log(e); }
          app.Y.fire('gridloader:griddata_fetched');
          _me.handle_gridunit_data(request.grid_id,json);
        },
        failure:function(){
          app.Y.fire('gridloader:griddata_fetched');
        }
      }
    }
  );
}

tc.griddr.gridloader.prototype.handle_gridunit_data = function(grid_id,d){
  //tc.util.log('tc.griddr.gridloader.prototype.handle_gridunit_data');
  this.cached_gridunit_data[grid_id] = d;
  app.fire('gridloader:gridunit_loaded',{grid_id:grid_id, gridunit_data:d});
}