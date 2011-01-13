import org.json.*;

APILoader loader;
 
void setup(){
  size(500,375);
  frameRate(1);
  loader = new APILoader(this);
}
 
void draw() {
  if(frameCount % 5){
    loader.request("http://localhost:8888/api/info/");
  }
  if(loader.responses.size() > 0) {
    handle_response(loader.get_response());
  }
}

void handle_response(JSONObject response){
  text(response.toString(),100,100);
}
