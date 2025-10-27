import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Klasa początkowa programu, wczytująca główne okno
 */
public class FiguryPaintApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoaderMain = new FXMLLoader(getClass().getResource("/MainWindow.fxml"));
        Scene mainScene = new Scene(fxmlLoaderMain.load(), 600, 695);
        stage.setResizable(false);
        stage.setTitle("FiguryPaint");
        stage.setScene(mainScene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}