package ui;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class Application extends javafx.application.Application {

    Scene loginScene;
    Stage mainStage;
    LoginMenuController loginMenuController;

    public void start(Stage stage) throws IOException {

        FXMLLoader fxmlLoaderMain = new FXMLLoader(getClass().getResource("LoginMenu.fxml"));
        loginScene = new Scene(fxmlLoaderMain.load());
        loginMenuController = fxmlLoaderMain.getController();


        stage.setResizable(false);
        stage.setTitle("Menu");
        stage.setScene(loginScene);
        stage.show();
        mainStage = stage;
        loginMenuController.setStage(mainStage);
    }

    public void start(String[] args) {
        launch(args);
    }

}
