import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Klasa początkowa programu, wczytująca główne okno.
 */
public class BinaryTreeClientFXApplication1 extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoaderMain = new FXMLLoader(getClass().getResource("BinaryTreeWindow.fxml"));
        Scene mainScene = new Scene(fxmlLoaderMain.load());

        stage.setResizable(false);
        stage.setTitle("Menu");
        stage.setScene(mainScene);
        stage.show();
    }

    /**
     * Główna metoda uruchamiająca aplikację.
     */
    public static void main(String[] args) {
        launch();
    }
}
