package ui;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

import java.net.URL;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ResourceBundle;

public class MainWindowController implements Initializable {

    private Boolean isAdmin;

    @FXML
    Label pracownikOrAdmin;

    @FXML
    ComboBox<String> polecenieComboBox;

    @FXML
    Label infoLabel;

    @FXML
    TextField inputTextField;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        if(isAdmin = setAdmin()){
            pracownikOrAdmin.setText("Zalogowany jako admin");
        }else {
            pracownikOrAdmin.setText("Zalogowany jako pracownik");
        }

        try{
            Statement statement = DatabaseConnection.getInstance().getConnection().createStatement();
            statement.executeQuery("CALL stworzLog(\"Zalogowano\")");
        }catch (Exception e){
            e.printStackTrace();
        }

        polecenieComboBox.setOnAction(actionEvent -> {
            String selectedValue = polecenieComboBox.getValue();
            switch (selectedValue) {
                case "Dowolna kwerenda":
                    infoLabel.setText("Tu możesz wpisać dowolną kwerendę");
                    break;
                case "Wypożycz samochód":
                    infoLabel.setText("<numer telefonu wyporzyczającego>,<numer rejestracji wyporzyczanego samochodu>,<na ile dni>");
                    break;
                case "Zarejestruj nowy samochód":
                    infoLabel.setText("<marka samochodu>,<model samochodu>,<rok produkcji samochodu>,<nr rejestracji samochodu>,<koszt na dzien wyporzyczenia>");
                    break;
                case "Zarejestruj płatność":
                    infoLabel.setText("<numer telefonu klienta>,<numer rejestracji samochodu>");
                    break;
                case "Sprawdź czy klient ma coś do zapłaty":
                    infoLabel.setText("<numer telefonu>");
                    break;
                case "Zarejestruj nowego pracownika":
                    infoLabel.setText("<imie>,<nazwisko>,<nazwa użytkownika>");
                    break;
                case "Zarejestruj nowego klienta":
                    infoLabel.setText("<pesel>,<imie>,<nazwisko>,<numer telefonu>");
                    break;
                case "Usuń klienta":
                    infoLabel.setText("<nr telefonu>");
                    break;
                case "Usuń samochod":
                    infoLabel.setText("<nr rejestracji>");
                    break;
                default:
                    infoLabel.setText("brak argumentów");
                    break;
            }
            inputTextField.setText("");
        });

        fillOutComboBox();
    }

    private void fillOutComboBox(){
        if(isAdmin){
            polecenieComboBox.getItems().addAll(
                    "Dowolna kwerenda",
                    "Wypożycz samochód",
                    "Zarejestruj nowy samochód",
                    "Zarejestruj płatność",
                    "Sprawdź dostepne samochody",
                    "Sprawdź czy klient ma coś do zapłaty",
                    "Zarejestruj nowego pracownika",
                    "Zarejestruj nowego klienta",
                    "Usuń klienta",
                    "Usuń samochod",
                    "Zobacz tabele klienci",
                    "Zobacz tabele samochody",
                    "Zobacz tabele wypozyczenia",
                    "Zobacz tabele platnosci",
                    "Zobacz tabele pracownicy",
                    "Zobacz tabele logi");
        }else {
            polecenieComboBox.getItems().addAll(
                    "Wypożycz samochód",
                    "Zarejestruj nowy samochód",
                    "Zarejestruj płatność",
                    "Usuń klienta",
                    "Usuń samochod",
                    "Sprawdź dostepne samochody",
                    "Sprawdź czy klient ma coś do zapłaty",
                    "Zarejestruj nowego klienta",
                    "Zobacz tabele klienci",
                    "Zobacz tabele samochody",
                    "Zobacz tabele wypozyczenia",
                    "Zobacz tabele platnosci");
        }
    }

    public Boolean setAdmin()  {

        try {
            String query = "SHOW GRANTS";

            Statement statement = DatabaseConnection.getInstance().getConnection().createStatement();
            ResultSet resultSet = statement.executeQuery(query);

            while (resultSet.next()) {
                String grant = resultSet.getString(1);
                if (grant.toUpperCase().contains("CREATE")) {
                    return true;
                }
            }

        }catch (Exception e){
            e.printStackTrace();
        }
        return false;
    }

    public void wykonajButtonClick(){
        DatabaseConnection.getInstance().sendQuery(polecenieComboBox.getValue(),inputTextField.getText());
    }
}
