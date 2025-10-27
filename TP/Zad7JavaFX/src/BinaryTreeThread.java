import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class BinaryTreeThread extends Thread {

    private Socket socket;
    private  BinaryTree<Integer> intTree;
    private  BinaryTree<Double> doubleTree;
    private  BinaryTree<String> stringTree ;
    private String TreeType;

    public BinaryTreeThread(Socket Socket){
        socket = Socket;
    }

    @Override
    public void run() {
        try (
                BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter output = new PrintWriter(socket.getOutputStream(),true)
        ) {
            intTree = new BinaryTree<>();
            doubleTree = new BinaryTree<>();
            stringTree = new BinaryTree<>();
            TreeType = "Integer";
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
        switch (TreeType) {
            case "Integer":
                intTree.insert(Integer.parseInt(value));
                break;
            case "Double":
                doubleTree.insert(Double.parseDouble(value));
                break;
            case "String":
                stringTree.insert(value);
                break;
        }
    }

    private void delete(String value) {
        switch (TreeType) {
            case "Integer":
                intTree.delete(Integer.parseInt(value));
                break;
            case "Double":
                doubleTree.delete(Double.parseDouble(value));
                break;
            case "String":
                stringTree.delete(value);
                break;
        }
    }

    private boolean search(String value) {
        switch (TreeType) {
            case "Integer":
                return intTree.search(Integer.parseInt(value));
            case "Double":
                return doubleTree.search(Double.parseDouble(value));
            case "String":
                return stringTree.search(value);
        }
        return false;
    }

    private String getTreeData() {
        switch (TreeType) {
            case "Integer":
                return intTree.drawTree();
            case "Double":
                return doubleTree.drawTree();
            case "String":
                return stringTree.drawTree();
        }
        return "";
    }
}
