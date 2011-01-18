if(!tc){ var tc = {}; }

tc.user = makeClass();

tc.user.prototype.init = function(app,options){
  tc.util.log('tc.user.prototype.init');
  this.get_current_user();
}

tc.user.prototype.get_current_user = function(){
  tc.util.log('tc.user.prototype.get_current_user');
  app.Y.io('/user/current/',
    {
      method:"POST",
      on:{
        success:function(transactionId, response, arguments){
          var json;
          try{
            json = app.Y.JSON.parse(response.responseText);
          } catch(e){ tc.util.log(e); return; }
          app.infopane.update('Logged in as',json.email);
          app.infopane.update('Logout',"<a href='/logout/'>here</a>");
          app.fire('user:user-loaded',json);
        },
        failure:function(){
          document.location = '/';
          app.fire('user:user-not-authenticated');
        }
      }
    }
  );
}