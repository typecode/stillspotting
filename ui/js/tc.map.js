if(!tc){ var tc = {}; }

tc.map = function(){
  
  _me = this;
  
  this.initialize = function(){
    tc.util.log('map.initialize');
    return _me;
  }
  
  return this.initialize();
}