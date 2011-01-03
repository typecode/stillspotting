if(!tc){ var tc = {}; }

tc.infopane = makeClass();

tc.infopane.prototype.markup = '<div class="infopane">\
    <ul></ul>\
  </div>';

tc.infopane.prototype.init = function(app,options){
  tc.util.log('tc.infopane.prototype.init');
  this.units = {};
  this.dom = app.Y.Node.create(this.markup);
  this.dom._node.setAttribute('id', 'infopane-'+Math.floor(Math.random()*10000));  
  app.dom.append(this.dom);
}
  
tc.infopane.prototype.update = function(name,value,options){
  //tc.util.log('tc.infopane.prototype.update');
  if(!name || !value){
    return false;
  }
  if(!this.units[name]){
    this.units[name] = app.Y.Node.create('<li><p>\
      <span class="name"></span>:\
      <span class="value"><span>\
    </p></li>');
    this.units[name].one('.name')._node.innerHTML = name;
    this.dom.one('ul').append(this.units[name]);
  }
  this.units[name].one('.value')._node.innerHTML = value;
}
