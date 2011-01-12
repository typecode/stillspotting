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
  this.editor = null;
  this.editor_status = null;
  this.codemirror = null;
  this.dom = app.Y.Node.create(this.markup);
  this.table = this.dom.one('table');
  this.table.append(this.build_api_selector());
  this.table.append(this.build_json_input());
  this.table.append(this.build_submit_button());
  this.setup_events();
  app.dom.append(this.dom);
  
  this.codemirror = this.construct_codemirror(function(){
    app.infopane.update('API Query Editor','Started');
    _me.codemirror.setCode('{"loaded":true}');
  },function(){
    try{
      app.Y.JSON.parse(_me.codemirror.getCode());
      _me.editor_status._node.innerHTML = 'SYNTAX OK!';
    } catch(e){
      _me.editor_status._node.innerHTML = 'BAD SYNTAX!';
      return;
    }
  });
}

tc.api.form.prototype.build_api_selector = function(){
  tc.util.log('tc.api.form.prototype.build_api_selector');
  return "<tr>\
    <th>\
      <label>Select an API:</label>\
    </th>\
    <td>\
      <select>\
        <option value='generic'>generic</option>\
        <option value='nytarticle'>nyt article</option>\
        <option value='nytcomments'>nyt comments</option>\
        <option value='nytnewswire'>nyt newswire</option>\
        <option value='googlegeocode'>google geocode</option>\
      </select>\
    </td>\
  </tr>";
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
    onLoad:loadcallback,
    onChange:changecallback
  });
  return codemirror;
}


tc.api.form.prototype.build_submit_button = function(){
  tc.util.log('tc.api.form.prototype.build_submit_button');
  return "<tr>\
    <th></th>\
    <td>\
      <input class='submit-button' type='submit' value='submit></input>\
    </td>\
  </tr>";
}


tc.api.form.prototype.setup_events = function(){
  tc.util.log('tc.api.form.prototype.setup_events');
  var _me;
  _me = this;
  this.dom.one('.submit-button').on('click',function(event){
    tc.util.log('tc.api.form.prototype.setup_events(click)');
    var data;
    event.preventDefault();
    data = {};
    data.api = _me.dom.one('select')._node.value;
    data.query = _me.codemirror.getCode();
    app.fire('api-form:form-submitted',data);
  });
}

tc.api.form.prototype.submit_click_handler = function(event){
  tc.util.log('tc.api.form.prototype.submit_click_handler');
  var data;
  event.preventDefault();
  data.api = this.dom.one('select')._node.value;
  data.query = this.codemirror.getCode();
  app.fire('api-form:form-submitted',data);
}

