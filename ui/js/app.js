if(!tc){ var tc = {}; }

var app = {
    Y:null,
    selector:'#app',
    name:'typecode-experiements',
    version:0.1
  }
  
  app.initialize = function(Y){
    tc.util.log('app.initialize');
    app.Y = Y;
    app.Y.augment(this, Y.EventTarget, null, null, {});
    app.dom = app.Y.one(app.selector);
    
    app.setup_submission_form();
    
    app.infopane = new tc.infopane(app,{});
    app.infopane.update('App Status',"starting");
    
    app.map = new tc.gmap(app,{});
    app.viz = new tc.viz(app,{});
    
    app.griddr = new tc.griddr(app,{});
    app.viz.addLayer(app.griddr.getView());
    
    app.loader = new tc.griddr.gridloader(app,{});
    
    app.infopane.update('App Status',"started");
  }
  
  app.setup_submission_form = function(){
    app.Y.one('#submit_button').on('click',function(e){
      e.preventDefault();
      app.Y.io('/article/comments',
        { data:'url='+app.Y.one('#article_url').get('value'),
          on:{
          success:function(transactionId, response, arguments){
            var json, i;
            try{
              json = app.Y.JSON.parse(response.responseText);
              if(json.req_id){
                app.listen_for_updates(json.req_id);
              }
            }catch(error){
              tc.util.log(error);
            }
          }
        }}
      );
    })
  }
  
  app.listen_for_updates = function(req_id){
    app.Y.io('/article/updates',
        { data:'req_id='+req_id,
          on:{
          success:function(transactionId, response, arguments){
            var json, i;
            try{
              json = app.Y.JSON.parse(response.responseText);
              if(json.comments){
                app.viz.renderComments(json.comments)
              }
              if(json.articles){
                
              }
              app.listen_for_updates(req_id)
            }catch(error){
              tc.util.log(error);
              app.listen_for_updates(req_id)
            }
          }
        }}
      );
  }
  