if(!tc){ var tc = {}; }

tc.api.info = makeClass();

tc.api.info.prototype.markup = "<div class='api-info'>\
  <div class='hd'></div>\
  <div class='bd'></div>\
  <div class='ft'></div>\
</div>";

tc.api.info.prototype.init = function(app,options){
  tc.util.log('tc.api.info.prototype.init');
  this.api_info = null;
  this.dom = app.Y.Node.create(this.markup);
  if(options.width){
    this.dom.addClass(options.width).addClass('column');
  }
  app.Y.one(options.target_element).append(this.dom);
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
  var _me, parameters_table, i, par;
  
  if(api.length == 0){
    this.dom.one('.bd')._node.innerHTML = "";
    this.dom.one('.bd').append('<h2>Getting Started</h2><br/>');
    this.dom.one('.bd').append('<p>◀ Get started by selecting an API/Data Source to the left.</p><br />');
    this.dom.one('.bd').append('<p class="italic">Keep in mind:</p>');
    this.dom.one('.bd').append('<p class="padded">&para;&nbsp;Certain API requests might take a few moments to complete. As a general rule, the greater the number of results you request, the longer the request will take. \
      &para;&nbsp;Certain APIs may require authentication to retrieve your and your friend\'s information, tweets, checkins, etc. \
      &para;&nbsp;The CSV Output is formatted with tabs (\\t) seperating values, and newlines (\\n) seperating rows. \
      &para;&nbsp;The Data Tool is still a work in progress. Things may behave erratically, but will evolve quickly. \
      &para;&nbsp;Please get in touch with questions comments suggestions: amahon[at]gmail.com. \
    </p><br />');
    this.dom.one('.bd').append('<p class="italic">On the way:</p>');
    this.dom.one('.bd').append('<p class="padded">&para;&nbsp;More API connections: Foursquare, Facebook. \
      &para;&nbsp;More thorough API results data in CSV output. \
      &para;&nbsp;Better documentation. \
      &para;&nbsp;You tell me!\
    </p>');
    //this.dom.one('.bd').append('<p>&raquo;Certian APIs may require authentication.</p>');
    return;
  }
  
  if(!this.api_info){ return; }
  if(!this.api_info[api]){
    return;
  }
  _me = this;
  
  this.dom.one('.bd')._node.innerHTML = "";
  this.dom.one('.bd').append('<h2>'+this.api_info[api].name+'</h2>');
  this.dom.one('.bd').append('<p>'+this.api_info[api].description+'</p><br />');
  if(this.api_info[api].authorized === false){
    this.dom.one('.bd').append('<p class="alert">You must <a href="/api/'+api+'/auth/">authenticate</a> to use this API.</p><br />');
  }
  
  this.dom.one('.bd').append('<p><a href="#" class="pop_default">◀ Populate Example Query</a></p><br />');
  this.dom.one('.pop_default').on('click',function(event){
    var code, i;
    event.preventDefault();
    code = _me.api_info[api].example_query;
    code = app.Y.JSON.stringify(code,null,"\t");
    app.fire('api-info:api-code-generated',{code:code});
  });
  
  app.fire('api-info:api-code-generated',{code:app.Y.JSON.stringify(_me.api_info[api].example_query,null,"\t")});
  
  this.dom.one('.bd').append('<p>Query Parameters:</p><br />');
  parameters_table = app.Y.Node.create('<table class="parameter_table">\
  </table>');
  for(i in this.api_info[api].default_pars){
    par = this.api_info[api].default_pars[i];
    details = ""
    details = details + '<p><strong>Required:</strong> '+par.required+"</p>";
    details = details + '<p><strong>Accepted:</strong> '+par.accepted+"</p>";
    if(par.default){
      details = details + '<p><strong>Default:</strong> '+par.default+"</p>";
    }
    if(par.more_info){
      details = details + '<p><strong>More Info:</strong> <a href="'+par.more_info+'">here</a></p>';
    }
    parameters_table.append('<tbody>\
      <tr>\
        <th colspan="2">'+i+'</th>\
      </tr><tr>\
        <td colspan="2">'+details+'</td>\
      </tr>\
    </tbody>')
  }
  this.dom.one('.bd').append(parameters_table);
  if(this.api_info[api].source){
    this.dom.one('.bd').append('<p class="italic">(Source: <a href="'+this.api_info[api].source+'">'+this.api_info[api].source+'</a>)</p>');
  }
  
  //this.dom.append('<pre>'+app.Y.JSON.stringify(this.api_info[api].default_pars,null,'&nbsp;&nbsp;')+'</pre>');
}
