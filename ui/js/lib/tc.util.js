/******************************************/
/******************************************/
/****  JS Document                     ****/
/****  by Andrew Mahon                 ****/
/****  amahon@gmail.com                ****/
/******************************************/
/******************************************/

if(!tc){ var tc = {}; }

(function(tc) {
	tc.util = {};
	tc.util.log = function(message,level){
		if (typeof console != "undefined" && typeof console.debug != "undefined") {
			if(!level){
				console.info(message)
			} else {
				console[level](message)
			}
		}
	}
	tc.util.dump = function(object){
		if (typeof console != "undefined" && typeof console.debug != "undefined") {
			console.log(object)
		}
	}
})(tc);


// makeClass - By John Resig (MIT Licensed)
function makeClass(){
  return function(args){
    if ( this instanceof arguments.callee ) {
      if ( typeof this.init == "function" )
        this.init.apply( this, args.callee ? args : arguments );
    } else
      return new arguments.callee( arguments );
  };
}