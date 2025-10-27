package ui;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class LoginMenuController {

    private Stage stage;

    @FXML
    TextField loginTextField;

    @FXML
    TextField passwordTextField;

    @FXML
    TextField loginButton;

    public void login(){

        String user = loginTextField.getText();
        String password = passwordTextField.getText();

        boolean result = DatabaseConnection.getInstance().connect(user, password);

        if (result){
            showWindow();
            System.out.println("Zalogowano");
        }else {
            loginTextField.setText("");
            passwordTextField.setText("");
            System.out.println("Błędne dane logowania");
        }

    }

    public void setStage(Stage stage) {
        this.stage = stage;
    }

    private void showWindow() {
        try{
            FXMLLoader fxmlLoaderMain = new FXMLLoader(getClass().getResource("MainWindow.fxml"));
            Scene scene = new Scene(fxmlLoaderMain.load());
            stage.setScene(scene);
            stage.setTitle("");
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
