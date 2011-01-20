if(!tc){ var tc = {}; }

tc.api.form = makeClass();

tc.api.form.prototype.markup = "<form class='api-form'>\
    <table>\
      <tr>\
        <th width='30%'></th>\
        <td width='70%'></td>\
    </table>\
  </form>";

tc.api.form.prototype.init = function(app,options){
  tc.util.log('tc.api.form.prototype.init');
  app.infopane.update('API Query Editor','Starting');
  var _me;
  _me = this;
  this.api_selector = null;
  this.editor = null;
  this.editor_status = null;
  this.submit_button = null;
  this.query_valid = false;
  this.codemirror = null;
  this.submit_button = null;
  this.dom = app.Y.Node.create(this.markup);
  this.table = this.dom.one('table');
  this.table.one('tbody').append(this.build_api_selector());
  this.table.one('tbody').append(this.build_json_input());
  this.table.one('tbody').append(this.build_submit_button());
  app.dom.append(this.dom);
  
  this.setup_events();
  
  this.codemirror = this.construct_codemirror(function(){
    app.infopane.update('API Query Editor','Started');
  },function(){
    try{
      app.Y.JSON.parse(_me.codemirror.getCode());
      _me.editor_status.addClass('okay').removeClass('error');
      _me.editor_status._node.innerHTML = 'SYNTAX OK!';
      //_me.submit_button.setAttribute('disabled',false);
      _me.query_valid = true;
    } catch(e){
      _me.editor_status.addClass('error').removeClass('okay');
      _me.editor_status._node.innerHTML = 'BAD SYNTAX!';
      //_me.submit_button.setAttribute('disabled',true);
      _me.query_valid = false;
      return;
    }
  });
}

tc.api.form.prototype.setup_events = function(){
  tc.util.log('tc.api.form.prototype.setup_events');
  var _me;
  _me = this;
  this.submit_button.on('click',function(event){
    tc.util.log('tc.api.form.prototype.setup_events(click)');
    var data;
    if(!_me.query_valid){ return; }
    event.preventDefault();
    data = {};
    data.api = _me.dom.one('select')._node.value;
    data.query = _me.codemirror.getCode();
    app.fire('api-form:form-submitted',data);
  });
  this.api_selector.on('change',function(event){
    event.target.get('options').each(function(){
      if(this.get('selected')){
        app.fire('api-form:api-selected',{api:this.get('value')});
        return false;
      }
    })
  });
  app.on('api-info:api-info-success',function(data){
    _me.populate_api_selector(data);
  });
  app.on('api-info:api-code-generated',function(data){
    if(_me.codemirror){
      _me.codemirror.setCode(data.code);
    }
  });
}

tc.api.form.prototype.build_api_selector = function(){
  tc.util.log('tc.api.form.prototype.build_api_selector');
  var element;
  element = app.Y.Node.create("<tr>\
    <th>\
      <label>Select an API:</label>\
    </th>\
    <td>\
      <select></select>\
    </td>\
  </tr>");
  this.api_selector = element.one('select');
  return element;
}

tc.api.form.prototype.populate_api_selector = function(data){
  tc.util.log('tc.api.form.prototype.populate_api_selector');
  var i;
  this.api_selector.append('<option value=""></option>');
  for(i in data){
    this.api_selector.append('<option value="'+i+'">'+data[i].name+'</option>');
  }
  this.api_selector.fire('change');
}

tc.api.form.prototype.build_json_input = function(){
  tc.util.log('tc.api.form.prototype.build_json_input');
  var element;
  element = app.Y.Node.create("<tr>\
    <th>\
      <label>Create your query:</label>\
    </th>\
    <td class='codemirror'>\
      <textarea class='editor'></textarea>\
    </td>\
  </tr>\
  <tr>\
    <th></th>\
    <td>\
      <p class='editor_status'></p>\
    </td>\
  </tr>");
  this.editor = element.one('.editor');
  this.editor_status = element.one('.editor_status');
  return element;
}

tc.api.form.prototype.construct_codemirror = function(loadcallback,changecallback){
  tc.util.log('tc.api.form.prototype.construct_codemirror');
  var codemirror;
  codemirror = CodeMirror.fromTextArea(this.editor._node, {
    parserfile: ["tokenizejavascript.js", "parsejavascript.js"],
    path: "js/lib/codemirror/",
    stylesheet: "css/tc.jseditor.css",
    reindentOnLoad:true,
    indentUnit:0,
    onLoad:loadcallback,
    onChange:changecallback
  });
  return codemirror;
}

tc.api.form.prototype.build_submit_button = function(){
  tc.util.log('tc.api.form.prototype.build_submit_button');
  var element;
  element = app.Y.Node.create("<tr>\
    <th></th>\
    <td>\
      <input class='submit-button' type='submit' value='Run Query'></input>\
    </td>\
  </tr>");
  this.submit_button = element.one('input');
  return element;
}

tc.api.form.prototype.submit_click_handler = function(event){
  tc.util.log('tc.api.form.prototype.submit_click_handler');
  var data;
  event.preventDefault();
  data.api = this.dom.one('select')._node.value;
  data.query = this.codemirror.getCode();
  app.fire('api-form:form-submitted',data);
}

