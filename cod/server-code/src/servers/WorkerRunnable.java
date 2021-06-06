package servers;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.Socket;
import java.util.concurrent.TimeUnit;


@SuppressWarnings("unused")
public class WorkerRunnable implements Runnable{

    protected Socket clientSocket = null;
    protected String serverText   = null;

    public WorkerRunnable(Socket clientSocket, String serverText) {
        this.clientSocket = clientSocket;
        this.serverText   = serverText;
    }

    public void run() {
        try {
        	String response = "Respuesta desde el servidor.\n\n";
        	byte[] responseBytes = response.getBytes();
            InputStream input  = clientSocket.getInputStream();
            OutputStream output = clientSocket.getOutputStream();
            java.util.Date date = new java.util.Date();
            long timeBef = System.currentTimeMillis();
            long timeEnd;
            this.perderTiempo();
            this.IOuse();
            output.write(("HTTP/1.1 200 OK\nContent-Length: " + responseBytes.length + "\n\nRespuesta desde el servidor.\n\n").getBytes());
            output.close();
            input.close();
            timeEnd = System.currentTimeMillis();
            System.out.println(date.toString() + " | Request processed: " + (timeEnd - timeBef)/1000 +
            		" seconds " + (timeEnd - timeBef)%1000 + " milliseconds.");
            
        } catch (IOException e) {
        	
            e.printStackTrace();
            
        }
    }
    
    public void perderTiempo() {
    	int i, res;
    	for(i = 10, res = 1; i >= 1; i--) {
    		res *= i;
    	}
    }
    
    public void IOuse() {
    	
    	int i;
    	
    	try {
	    	File IO = new File("IOfile.txt");
	        if (IO.createNewFile()) {
	          System.out.println("File created: " + IO.getName());
	        }
		} catch (IOException e) {
    			System.out.println("Error during file creation.");
    			e.printStackTrace();
		}
    	
    	try {
    	      FileWriter myWriter = new FileWriter("IOfile.txt");
    	      for(i = 0; i < 100; i++) {
    	    	  myWriter.write("Texto de ejemplo");
    	      }
    	      myWriter.close();
	    } catch (IOException e) {
    	      System.out.println("Error during file edition.");
    	      e.printStackTrace();
	    }
    }
}