import org.json.JSONObject;
import org.json.JSONException;

class APILoader implements DataLoadCallback {
 
  PApplet parentapp;
  ArrayList<JSONObject> responses;
 
  APILoader(PApplet app) {
    println("APILoader");
    parentapp = app;
    responses = new ArrayList<JSONObject>();
  }
  
  void request(String url){
    println("APILoader.request");
    CachedDataLoadQueue queue;
    queue=new CachedDataLoadQueue(parentapp, new String[]{url}, null);
    queue.setCallback(this);
    queue.start();
  }
  
  JSONObject get_response(){
    println("APILoader.get_response");
    JSONObject response = responses.get(0);
    responses.remove(0);
    return response;
  }
 
  void itemLoaded(DataBuffer buffer) {
    println("APILoader.itemLoaded");
  }
 
  void itemFailed(Exception e) {
    println("APILoader.itemFailed");
  }
 
  void queueComplete(DataBuffer[] buffers) {
    println("APILoader.queueComplete");
    for(int i=0; i<buffers.length; i++) {
      JSONObject response;
      try{
        response = new JSONObject(buffers[i].getAsText());
        responses.add(response);  
      } catch (JSONException e){
        println ("There was an error parsing the JSONObject.");
      }
    }
  }
}
