package servers;

import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.IOException;
import java.util.ServiceConfigurationError;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PoolThreadedServer implements Runnable{

    protected int          		serverPort    = 8080;
    protected int 				maxClient	  = 50;
    protected InetAddress 		addr;
    protected ServerSocket 		serverSocket  = null;
    protected boolean      		isStopped     = false;
    protected Thread       		runningThread = null;
    protected ExecutorService 	threadPool    = Executors.newFixedThreadPool(50);

    public PoolThreadedServer(int port){
        this.serverPort = port;
    }

    public void run(){
        synchronized(this){
            this.runningThread = Thread.currentThread();
        }
        
        getIPaddr();
        openServerSocket();
        
        Socket clientSocket = null;
        
        while(!isStopped()){
        	
        	clientSocket = null;
            
            try {
                clientSocket = this.serverSocket.accept();
            } catch (IOException e) {
                if(isStopped()) {
                    System.out.println("Server Stopped.") ;
                    break;
                }
                throw new RuntimeException(
                    "Error accepting client connection", e);
            }
            
            this.threadPool.execute(new WorkerRunnable(clientSocket, "Thread Pooled Server"));
            
        }
        
        try {
			clientSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
        
        this.threadPool.shutdown();
        System.out.println("Thread Stopped.") ;
    }


    private void getIPaddr() {
    	try {
    		addr  = InetAddress.getByName("192.168.1.46");
    	}catch(UnknownHostException e){
    		throw new ServiceConfigurationError(e.toString(),e);
    	}	
	}

	private synchronized boolean isStopped() {
        return this.isStopped;
    }

    public synchronized void stop(){
        this.isStopped = true;
        try {
            this.serverSocket.close();
        } catch (IOException e) {
            throw new RuntimeException("Error closing server", e);
        }
    }

    private void openServerSocket() {
        try {
            this.serverSocket = new ServerSocket(this.serverPort, this.maxClient, this.addr);
        } catch (IOException e) {
            throw new RuntimeException("Cannot open port 8080", e);
        }
    }
    
    public static void main(String[] args) {
		
		PoolThreadedServer server = new PoolThreadedServer(8080);
		
		new Thread(server).start();
		System.out.println("Server started...");
		try {
		    Thread.sleep(Long.MAX_VALUE);
		} catch (InterruptedException e) {
		    e.printStackTrace();
		}
		System.out.println("Stopping Server");
		server.stop();

	}
}
