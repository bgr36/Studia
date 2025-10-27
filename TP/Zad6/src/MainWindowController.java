import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

/**
 * Kontroler dla głównego okna aplikacji.
 * Obsługuje wczytywanie parametrów i otwieranie okna siatki.
 */
public class MainWindowController {

    /**
     * Główna scena aplikacji.
     */
    Stage MainStage;

    static int m = 0;
    static int n = 0;
    static int k = 0;
    static double p = 0;

    @FXML
    private Label OutputLabel;

    @FXML
    private TextField MTextField;

    @FXML
    private TextField NTextField;

    @FXML
    private TextField KTextField;

    @FXML
    private TextField PTextField;


    /**
     * Obsługuje kliknięcie przycisku "Generate" i otwiera nowe okno z siatką.
     */
    public void GenerateButtonClicked() {
        try {
            m = Integer.parseInt(MTextField.getText());
            n = Integer.parseInt(NTextField.getText());
            p = Double.parseDouble(PTextField.getText());
            k = Integer.parseInt(KTextField.getText());
        } catch (Exception e) {
            OutputLabel.setText("Błędne dane");
            return;
        }

        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("GridWindow.fxml"));
            Parent root = loader.load();

            GridWindowController controller = loader.getController();

            Stage stage = new Stage();

            stage.setResizable(false);
            stage.setScene(new Scene(root));
            GridWindowController.m = m;
            GridWindowController.n = n;
            controller.p = p;
            controller.k = k;
            controller.GenerateGrid();

            stage.show();
           //MainStage.close();
            OutputLabel.setText("Podaj parametry");
        } catch (Exception e) {
            OutputLabel.setText("Błąd wczytywania sceny");
        }
    }

    /**
     * Ustawia główną scenę aplikacji.
     */
    public void setMainStage(Stage stage) {
        this.MainStage = stage;
    }
}

