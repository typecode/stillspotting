if(!tc){ var tc = {}; }

tc.api.loader = makeClass();

tc.api.loader.prototype.init = function(app,options){
  tc.util.log('tc.api.loader.prototype.init');
  this.setup_events();
}

tc.api.loader.prototype.setup_events = function(){
  tc.util.log('tc.api.loader.prototype.setup_events');
  var _me;
  _me = this;
  app.on('api-form:form-submitted',function(data){
    _me.execute_query(data);
  });
}

tc.api.loader.prototype.execute_query = function(data){
  tc.util.log('tc.api.loader.prototype.execute_query');
  var _me, url, query;
  _me = this;
  if(!data.api){ return; }
  if(!data.query){ return; }
  url = '/api/'+data.api+'/';
  try{
    data.query = app.Y.JSON.parse(data.query);
  } catch(e){
    app.fire('api-loader:api-query-syntax-error');
    return;
  }
  url = url + '?' +app.Y.QueryString.stringify(data.query);
  app.fire('api-loader:api-query-started',{url:url});
  app.Y.io(url,
    {
      method:'GET',
      on:{
        success:function(transactionId, response, arguments){
          var json;
          try{
            json = app.Y.JSON.parse(response.responseText);
          } catch(e){ tc.util.log(e); return; }
          app.fire('api-loader:api-data-success',{data:json,url:url});
        },
        failure:function(){
          app.fire('api-loader:api-data-error',{url:url});
        }
      }
    }
  );
}