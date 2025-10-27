
import java.io.*;
import java.net.Socket;

public class BinaryTreeServerThread extends Thread {

    private Socket socket;
    private final static BinaryTree<Integer> intTree = new BinaryTree<>();
    private final static BinaryTree<Double> doubleTree = new BinaryTree<>();
    private final static BinaryTree<String> stringTree = new BinaryTree<>();
    private static String TreeType = "Integer";

    public BinaryTreeServerThread(Socket Socket){
        socket = Socket;
    }

    @Override
    public void run() {
        try (
                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter output = new PrintWriter(socket.getOutputStream(),true)
        ) {
            String command;
            while ((command = (String) input.readLine()) != null) {
                String[] parts = command.split(" ");
                String operation = parts[0];

                try{
                    System.out.println(intTree.root.elem + "" + intTree.root.left.elem + "" + intTree.root.right.elem );
                }catch (Exception e){

                }

                if (parts.length < 2 && !parts[0].equals("draw")) {
                    output.println("Niepoprawne polecenie");
                    continue;
                }

                switch (operation) {
                    case "setType":
                        TreeType = parts[1];
                        output.println("Typ drzewa ustawiony do " + TreeType);
                        break;
                    case "insert":
                        insert(parts[1]);
                        output.println("Wstawiono " + parts[1]);
                        break;
                    case "delete":
                        delete(parts[1]);
                        output.println("Usunieto " + parts[1]);
                        break;
                    case "search":
                        boolean found = search(parts[1]);
                        output.println(found ? "Znaleziono " + parts[1] : "Nie znaleziono " + parts[1]);
                        break;
                    case "draw":
                        output.println(getTreeData());
                        System.out.print(getTreeData());
                        break;
                    default:
                        output.println("Nieznane polecenie");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void insert(String value) {
        switch (TreeType){
            case "Integer":
                intTree.Insert(Integer.parseInt(value));
                break;
            case "Double":
                doubleTree.Insert(Double.parseDouble(value));
                break;
            case "String":
                stringTree.Insert(value);
                break;
        }
    }

    private void delete(String value) {
        switch (TreeType) {
            case "Integer":
                intTree.Delete(Integer.parseInt(value));
                break;
            case "Double":
                doubleTree.Delete(Double.parseDouble(value));
                break;
            case "String":
                stringTree.Delete(value);
                break;
        }
    }

    private boolean search(String value) {
        switch (TreeType) {
            case "Integer":
                return intTree.Search(Integer.parseInt(value));
            case "Double":
                return doubleTree.Search(Double.parseDouble(value));
            case "String":
                return stringTree.Search(value);
        }
        return false;
    }

    private String getTreeData() {
        switch (TreeType) {
            case "Integer":
                return intTree.Draw();
            case "Double":
                return doubleTree.Draw();
            case "String":
                return stringTree.Draw();
        }
        return "";
    }
}
