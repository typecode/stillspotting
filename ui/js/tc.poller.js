if(!tc){ var tc = {}; }

tc.poller = function(options){
  
  _me = this;
  
  this.initialize = function(){
    tc.util.log('poller.initialize');
    if(!options.uri){
      _me = false;
    }
    return _me;
  }
  
  this.poll = function(){
    tc.util.log('poller.poll');
    app.Y.io(options.uri,
      {on:{
        success:function(transactionId, response, arguments){
          var json, i;
          try{
            json = app.Y.JSON.parse(response.responseText);
            app.fire('poller:success',{data:json});
          }catch(error){
            tc.util.log(error);
          }
        }
      }}
    );
  }
  
  return this.initialize();
}