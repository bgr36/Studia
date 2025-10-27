import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.text.Text;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.URL;
import java.util.ResourceBundle;

public class BinaryTreeClientFX1 implements Initializable {

    private static BinaryTree<Integer> intTree = new BinaryTree<>();
    private static BinaryTree<Double> doubleTree = new BinaryTree<>();
    private static BinaryTree<String> stringTree = new BinaryTree<>();
    private PrintWriter output;
    private BufferedReader input;
    private static String TreeType = "Integer";
    @FXML
    private TextArea displayArea;
    @FXML
    private ComboBox<String> typeComboBox;
    @FXML
    private TextField inputField;
    @FXML
    private ScrollPane scrollPane;
    private Pane drawPane = new Pane();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        connectToServer();
        scrollPane.setContent(drawPane);
        scrollPane.setDisable(false);
    }

    private void connectToServer() {
        System.out.println("Zyje!");
        try {
            Socket socket = new Socket("localhost", 12345);
            output = new PrintWriter(socket.getOutputStream(),true);
            input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            displayArea.appendText("Połączono z serwerem\n");
            System.out.println("Połączono z serwerem");
        } catch (IOException e) {
            displayArea.appendText("Nie udało sie połączyć z serwerem\n");
            e.printStackTrace();
        }
    }

    public void setType() {
        String type = typeComboBox.getValue();
        sendCommand("setType " + type);
    }

    public void insert() {
        String value = inputField.getText();
        sendCommand("insert " + value);
    }

    public void delete() {
        String value = inputField.getText();
        sendCommand("delete " + value);
    }

    public void search() {
        String value = inputField.getText();
        sendCommand("search " + value);
    }

    public void draw() {
        sendCommand("draw");
    }

    void drawTree(String treeString){
        drawPane.getChildren().clear();
        String[] nodes = treeString.split(",");
        for (String node : nodes) {
            if (node.equals("null")) continue;

            String[] parts = node.split(" ");

            try {
                int x1 = Integer.parseInt(parts[1]);
                int y1 = Integer.parseInt(parts[2]);
                int x2 = Integer.parseInt(parts[3]);
                int y2 = Integer.parseInt(parts[4]);
                //System.out.println("Wartość:" + parts[0] + "X:" + x1 + "Y:" + y1);
                //System.out.println("Wartość:" + parts[0] + "X:" + x1 + "Y:" + y1 + "X:" + x2 + "Y:" + y2);
                Line line = new Line(x1,y1,x2,y2);
                Text text = new Text(x1, y1, parts[0]);
                Circle circle = new Circle(x1,y1,3);
                circle.setFill(Color.BLUEVIOLET);
                text.toFront();
                line.toBack();
                drawPane.getChildren().add(text);
                drawPane.getChildren().add(line);
                drawPane.getChildren().add(circle);
            } catch (NumberFormatException e) {
                System.out.println("Coś poszło nie tak przy rysowaniu drzewa");
            }
        }
    }

    private void sendCommand(String command) {
        try {
            output.println(command);
            String response = (String) input.readLine();
            if (command.startsWith("draw")) {
               drawTree(response);
            }else{
                displayArea.appendText(response + "\n");
            }
        } catch (IOException e) {
            displayArea.appendText("Błąd w komunikacji z serwerem\n");
            e.printStackTrace();
        }
    }



}
