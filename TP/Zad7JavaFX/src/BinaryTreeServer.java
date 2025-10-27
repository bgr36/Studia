import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class BinaryTreeServer {

        public static void main(String[] args) {

            try (ServerSocket serverSocket = new ServerSocket(12345)) {

                System.out.println("Server is listening on port 12345");

                while (true) {
                    Socket socket = serverSocket.accept();
                    System.out.println("New client connected");

                    new BinaryTreeThread(socket).start();
                }

            } catch (IOException ex) {
                System.out.println("Server exception: " + ex.getMessage());
                ex.printStackTrace();
            }
        }
}
