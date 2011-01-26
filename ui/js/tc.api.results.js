if(!tc){ var tc = {}; }

tc.api.results = makeClass();

tc.api.results.prototype.markup = "<div class='api-results'>\
  <div class='hd'></div>\
  <div class='bd'></div>\
  <div class='ft'></div>\
</div>";

tc.api.results.prototype.init = function(app,options){
  tc.util.log('tc.api.results.prototype.init');
  this.dom = app.Y.Node.create(this.markup);
  if(options.width){
    this.dom.addClass(options.width).addClass('column');
  }
  app.Y.one(options.target_element).append(this.dom);
  this.setup_events();
}

tc.api.results.prototype.setup_events = function(){
  tc.util.log('tc.api.results.prototype.setup_events');
  var _me;
  _me = this;
  app.on('api-loader:api-query-started', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p><strong>Please wait, query processing.</strong></p>");
  });
  app.on('api-loader:api-data-success', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p><strong>Query Loaded!</strong></p><br />");
    _me.dom.one('.bd').append("<p>Query Id: "+data.data.request_id+"</p>");
    if(data.data.format){
      _me.dom.one('.bd').append("<p>Output Format: "+data.data.format+"</p><br />");
    }
    _me.dom.one('.bd').append("<p><strong>Results:</strong></p>");
    results = "null"
    plaintext = "null"
    switch(data.data.format){
      case 'json':
        results = "<pre>"+app.Y.JSON.stringify(data.data.data,null,'  ')+"</pre>";
        plaintext = app.Y.JSON.stringify(data.data.data,null,'  ')
        break;
      case 'csv':
        results = _me.csv_to_table(data.data.data);
        plaintext = data.data.data
        break
      default:
        results = "No Output Formatter.";
        plaintext = data.data.data
        break;
    }
    _me.dom.one('.bd').append(results);
    _me.dom.one('.bd').append('<br />');
    _me.dom.one('.bd').append("<p><strong>Plain Text Results:</strong></p>");
    _me.dom.one('.bd').append("<textarea class='plaintext-results'>"+plaintext+"</textarea>");
  });
  app.on('api-loader:api-data-error', function(data){
    _me.dom.one('.bd')._node.innerHTML = "";
    _me.dom.one('.bd').append("<p>Error on: <a href='http://"+window.location.host+""+data.url+"'>http://"+window.location.host+""+data.url+"</a></p>");
    _me.dom.one('.bd').append("<pre>ERROR! PLEASE CHECK QUERY SYNTAX</pre>");
  });
}

tc.api.results.prototype.csv_to_table = function(csv){
  tc.util.log('tc.api.results.prototype.csv_to_table');
  var table,lines,i,j,table_width;
  table = app.Y.Node.create('<table class="csv-table">\
    <thead></thead>\
    <tbody></tbody>\
  </table>');
  lines = csv.split('\n');
  for(i in lines){
    lines[i] = lines[i].split('\t');
    if(i == 0){
      table_width = lines[i].length;
      row = '<tr>';
      for(j in lines[i]){
        row = row + '<th>'+lines[i][j]+'</th>';
      }
      row = row + '</tr>';
      table.one('thead')._node.innerHTML = table.one('thead')._node.innerHTML + row;
    } else {
      if(lines[i].length != table_width){
        tc.util.dump('Dropping row..');
        tc.util.dump(lines[i]);
        continue;
      }
      row = '<tr>';
      for(j in lines[i]){
        row = row + '<td>'+lines[i][j]+'</td>';
      }
      row = row + '</tr>';
      table.one('tbody')._node.innerHTML = table.one('tbody')._node.innerHTML + row;
    }
  }
  return table;
}

