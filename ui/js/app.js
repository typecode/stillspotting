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
    app.dom = app.Y.one(app.selector);
    app.setupevents();
    
    app.setup_submission_form();
    
    app.viz = tc.viz();
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
  
  app.setupevents = function(){
    tc.util.log('app.setupevents');
    app.Y.augment(app,app.Y.EventTarget);
    app.on('poller:success',function(e){
      var i,j;
      tc.util.dump(e.data);
      return;
      for(i in e.data.results){
        if(e.data.results[i].multimedia){
          for(j in e.data.results[i].multimedia){
            if(e.data.results[i].multimedia[j].url){
              app.dom.append('<img src="'+e.data.results[i].multimedia[j].url+'"></img>');
            }
          }
        }
        if(e.data.results[i].title){
          app.dom.append('<p>'+e.data.results[i].title+'</p>');
        }
      }
      app.poller.poll();
    });
  }
  