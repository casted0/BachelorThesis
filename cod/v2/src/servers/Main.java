package servers;

public class Main {

	public static void main(String[] args) {
		
		PoolThreadedServer server = new PoolThreadedServer(9000);
		// MultiThreadServer server = new MultiThreadServer(9000);
		
		new Thread(server).start();

		try {
		    Thread.sleep(20 * 1000);
		} catch (InterruptedException e) {
		    e.printStackTrace();
		}
		System.out.println("Stopping Server");
		server.stop();

	}

}
