if(!tc){ var tc = {}; }

tc.api.info = makeClass();

tc.api.info.prototype.markup = "<div class='api-info'></div>";

tc.api.info.prototype.init = function(app,options){
  tc.util.log('tc.api.info.prototype.init');
  this.api_info = null;
  this.dom = app.Y.Node.create(this.markup);
  app.dom.append(this.dom);
  this.setup_events();
  this.get_info(); 
}

tc.api.info.prototype.setup_events = function(){
  tc.util.log('tc.api.info.prototype.setup_events');
  var _me;
  _me = this;
  app.on('api-form:api-selected',function(data){
    _me.render_info_for(data.api);
  });
  app.on('api-info:api-info-success',function(data){
    _me.api_info = data;
  });
}

tc.api.info.prototype.get_info = function(){
  tc.util.log('tc.api.info.prototype.get_info');
  app.Y.io('/api/info/',
    {
      on:{
        success:function(transactionId, response, arguments){
          var json;
          try{
            json = app.Y.JSON.parse(response.responseText);
          } catch(e){ tc.util.log(e); return; }
          app.fire('api-info:api-info-success',json);
        },
        failure:function(){
          app.fire('api-info:api-info-error');
        }
      }
    }
  );
}

tc.api.info.prototype.render_info_for = function(api){
  tc.util.log('tc.api.info.prototype.render_info_for');
  var _me;
  if(!this.api_info){ return; }
  if(!this.api_info[api]){ 
    return; 
  }
  _me = this;
  
  this.dom._node.innerHTML = "";
  this.dom.append('<h2>'+this.api_info[api].name+'</h2>');
  this.dom.append('<p>'+this.api_info[api].description+'</p><br />');
  this.dom.append('<p><a href="#" class="pop_default">◀ Populate Default Query</a></p><br />');
  this.dom.one('.pop_default').on('click',function(event){
    var code, i;
    event.preventDefault();
    code = {}
    for(i in _me.api_info[api].default_pars){
      if(_me.api_info[api].default_pars[i].default){
        code[i] = _me.api_info[api].default_pars[i].default;
      }
      
    }
    code = app.Y.JSON.stringify(code,null," ");
    app.fire('api-info:api-code-generated',{code:code});
  })
  
  
  this.dom.append('<p>Query Parameters:</p>');
  this.dom.append('<pre>'+app.Y.JSON.stringify(this.api_info[api].default_pars,null,'&nbsp;&nbsp;')+'</pre>');
}
