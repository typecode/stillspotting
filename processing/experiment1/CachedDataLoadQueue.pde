/**
CachedDataLoadQueue taken from http://wiki.processing.org/w/Asynchronous_data/image_loading
@author toxi
*/

class CachedDataLoadQueue extends Thread {
  private DataLoadCallback caller;
  private Cache cache;
  private PApplet app;
  private String[] files;
  private DataBuffer[] buffers;
 
  private boolean isAlive = true;
 
  public int sleepTime = 30;
 
  public CachedDataLoadQueue(PApplet app, String[] files, Cache c) {
    this.app=app;
    this.files=files;
    buffers=new DataBuffer[files.length];
    cache=c;
  }
 
  // use this constructor if you don't need/want caching
  public CachedDataLoadQueue(PApplet app, String[] files) {
    this(app,files,null);
  }
 
  public void setCallback(DataLoadCallback cb) {
    caller=cb;
    if (caller==null) isAlive=false;
  }
 
  // some web APIs require a minimum delay between requests from the same IP
  // you can set this duration here (in milliseconds)...
  public void setSleepTime(int delay) {
    sleepTime=delay;
  }
 
  // main thread loop, triggered by the start() method
  public void run() {
    int id=0;
    while(isAlive && id<files.length) {
      try {
        String itemKey=files[id];
        DataBuffer buffer=cache!=null ? (DataBuffer)cache.retrieve(itemKey) : null;
        if (buffer==null) {
          byte[] bytes=app.loadBytes(itemKey);
          if (bytes!=null) {
            buffer=new DataBuffer(bytes);
            buffers[id]=buffer;
            if (cache!=null) cache.store(itemKey,buffer);
            if (caller!=null) caller.itemLoaded(buffer);
            Thread.sleep(sleepTime);
          } 
          else {
            isAlive=false;
            Exception e=new IOException("file not found: "+itemKey);
            if (caller!=null) caller.itemFailed(e);
            else e.printStackTrace();
            return;
          }
        } 
        else {
          buffers[id]=buffer;
        }
        id++;
      }
      catch(InterruptedException e) {
        break;
      }
    }
    if (isAlive) {
      if (caller!=null) caller.queueComplete(buffers);
    }
  }
 
  public DataBuffer[] getResultBuffers() {
    return buffers;
  }
}

/**
DataBuffer taken from http://wiki.processing.org/w/Asynchronous_data/image_loading
@author toxi
*/
 
import java.io.*;
import javax.imageio.*;
import java.awt.image.BufferedImage;
 
import processing.core.PImage;
 
public class DataBuffer {
 
  private byte[] bytes;
 
  public DataBuffer(byte[] buf) {
    bytes=buf;
  }
 
  public byte[] getRaw() {
     return bytes;
  }
 
  public String getAsText() {
    return getAsText("UTF-8");
  }
 
  public String getAsText(String encoding) {
    try {
      return new String(bytes,encoding);
    } 
    catch(Exception e) {
      e.printStackTrace();
    }
    return null;
  }
 
  // updated according to:
  // http://forum.processing.org/topic/converting-bufferedimage-to-pimage#25080000000340208
  public PImage getAsImage() {
    try {
      ByteArrayInputStream bis=new ByteArrayInputStream(bytes); 
      BufferedImage bimg = ImageIO.read(bis); 
      PImage img=new PImage(bimg.getWidth(),bimg.getHeight(),PConstants.ARGB);
      bimg.getRGB(0, 0, img.width, img.height, img.pixels, 0, img.width);
      img.updatePixels();
      return img;
    }
    catch(Exception e) {
      System.err.println("Can't create image from buffer");
      e.printStackTrace();
    }
    return null;
  }
}

/**
DataLoadCallback taken from http://wiki.processing.org/w/Asynchronous_data/image_loading
@author toxi
*/
public interface DataLoadCallback {
  public void itemLoaded(DataBuffer buffer);
  public void itemFailed(Exception e);
  public void queueComplete(DataBuffer[] buffers);
}
