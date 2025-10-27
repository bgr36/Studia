import java.io.*;
import java.net.*;
import java.util.Scanner;

public class BinaryTreeClient {

    private PrintWriter output;
    private BufferedReader input;
    private static String TreeType = "Integer";

    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 12345);
             PrintWriter output = new PrintWriter(socket.getOutputStream(),true);
             BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             Scanner scanner = new Scanner(System.in)) {

            System.out.println("Połączono z serwerem. Wpisz komendę:");

            while (scanner.hasNextLine()) {
                String command = scanner.nextLine();
                output.println(command);
                String response = (String) input.readLine();
                System.out.println("Wysłano komendę: " + command);
                if(command.equals("draw")){
                    Draw(response);
                }else{
                    System.out.print(response);
                    System.out.println(" ");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void Draw(String s){
        String[] lines = s.split(",");
        for (String str : lines){
            System.out.println(str);
        }
    }
}