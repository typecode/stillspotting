if(!tc){ var tc = {}; }

var app = {
    Y:null,
    selector:'#app',
    name:'typecode-experiements',
    version:0.1
  }
  
  app.initialize = function(Y,options){
    tc.util.log('app.initialize');
    app.Y = Y;
    app.Y.augment(this, Y.EventTarget, null, null, {});
    app.dom = app.Y.one(app.selector);
    
    //app.setup_submission_form();
    
    app.user = new tc.user(app,{});
    
    app.infopane = new tc.infopane(app,{});
    app.infopane.update('App Status',"starting");
    
    switch(options.view){
      case 'api':
        app.api = new tc.api(app,{});
        app.api.form = new tc.api.form(app,{
          width:'x3',
          target_element:'#form_tier'
        });
        app.api.info = new tc.api.info(app,{
          width:'x3',
          target_element:'#form_tier'
        });
        app.api.loader = new tc.api.loader(app,{});
        app.api.results = new tc.api.results(app,{
          width:'xFull',
          target_element:'#results_tier'
        });
        break;
      case 'map':
        app.map = new tc.gmap(app,{});
        app.viz = new tc.viz(app,{});
        app.griddr = new tc.griddr(app,{});
        app.loader = new tc.griddr.gridloader(app,{});
        app.gridmanager = new tc.griddr.gridmanager(app,{});
        //app.viz.addLayer(app.griddr.getView());
        //app.viz.addLayer(new tc.geoitem.view(app.map.instance));
        break;
      default:
        app.viewswitcher = new tc.viewswitcher(app,{});
        break;
    }
    
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
  