package ui;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import javafx.stage.Stage;

import java.sql.*;

public class DatabaseConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/wypozyczalniasamochodow";

    private Connection connection;

    public boolean connect(String user, String password) {
        try {
            connection = DriverManager.getConnection(URL, user, password);
            System.out.println("Połączenie z bazą danych zostało nawiązane.");
            return true;
        } catch (SQLException e) {
            System.err.println("Błąd podczas nawiązywania połączenia z bazą danych: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    public Connection getConnection() {
        return connection;
    }

    private DatabaseConnection() {
    }

    private static class SingletonHelper {
            static DatabaseConnection INSTANCE = new DatabaseConnection();
    }

    public static DatabaseConnection getInstance() {
        return SingletonHelper.INSTANCE;
    }

    public void sendQuery(String s,String params) {

        try {
            try {
                connection.setAutoCommit(false);
                String[] words = params.split(",");

                PreparedStatement statement;

                switch (s){
                    case "Dowolna kwerenda":
                        System.out.println("Dowolna kwerenda" + params);
                        statement = (PreparedStatement) connection.createStatement();
                        StringBuilder query = new StringBuilder();
                        query.append(params);
                        System.out.println(query.toString());
                        openNewWindow(statement.executeQuery(query.toString()));
                        return;
                    case "Wypożycz samochód":
                        System.out.println("Wypożycz samochód" + params);
                        statement = getConnection().prepareStatement("CALL wyporzycz_samochod(?,?,?)");
                        statement.setString(1,words[0]);
                        statement.setString(2,words[1]);
                        statement.setInt(3,Integer.parseInt(words[2]));
                        break;
                    case "Zarejestruj nowy samochód":
                        System.out.println("Zarejestruj nowy samochód" + params);
                        statement = getConnection().prepareStatement("CALL zarejestruj_samochod(?,?,?,?,?)");
                        statement.setString(1,words[0]);
                        statement.setString(2,words[1]);
                        statement.setInt(3,Integer.parseInt(words[2]));
                        statement.setString(4,words[3]);
                        statement.setInt(5,Integer.parseInt(words[4]));
                        break;
                    case "Zarejestruj płatność":
                        System.out.println("Zarejestruj płatność" + params);
                        statement = getConnection().prepareStatement("CALL dokonaj_platnosc(?,?)");
                        statement.setString(1,words[0]);
                        statement.setString(2,words[1]);
                        break;
                    case "Sprawdź dostepne samochody":
                        System.out.println("Sprawdź dostepne samochody" + params);
                        statement = getConnection().prepareStatement("CALL wyswietl_dostepne_samochody()");
                        break;
                    case "Sprawdź czy klient ma coś do zapłaty":
                        System.out.println("Sprawdź czy klient ma coś do zapłaty" + params);
                        statement = getConnection().prepareStatement("CALL czy_klient_ma_cos_do_zaplacenia(?)");
                        statement.setString(1,words[0]);
                        break;
                    case "Zarejestruj nowego pracownika":
                        System.out.println("Zarejestruj nowego pracownika" + params);
                        statement = getConnection().prepareStatement("CALL wprowadzPracownika(?,?,?)");
                        statement.setString(1,words[0]);
                        statement.setString(2,words[1]);
                        statement.setString(3,words[2]);
                        break;
                    case "Zarejestruj nowego klienta":
                        System.out.println("Zarejestruj nowego klienta" + params);
                        statement = getConnection().prepareStatement("CALL dodaj_klienta(?,?,?,?)");
                        statement.setString(1,words[0]);
                        statement.setString(2,words[1]);
                        statement.setString(3,words[2]);
                        statement.setString(4,words[3]);
                        break;
                    case "Usuń klienta":
                        statement = getConnection().prepareStatement("CALL usun_klienta(?)");
                        statement.setString(1,words[0]);
                        break;
                    case "Usuń samochod":
                        statement = getConnection().prepareStatement("CALL usun_samochod(?)");
                        statement.setString(1,words[0]);
                        break;
                    case "Zobacz tabele klienci":
                        statement = getConnection().prepareStatement("SELECT * FROM klienci");
                        break;
                    case "Zobacz tabele samochody":
                        statement = getConnection().prepareStatement("SELECT * FROM samochody");
                        break;
                    case "Zobacz tabele wypozyczenia":
                        statement = getConnection().prepareStatement("SELECT * FROM wypozyczenia");
                        break;
                    case "Zobacz tabele platnosci":
                        statement = getConnection().prepareStatement("SELECT * FROM platnosci");
                        break;
                    case "Zobacz tabele pracownicy":
                        statement = getConnection().prepareStatement("SELECT * FROM pracownicy");
                        break;
                    case "Zobacz tabele logi":
                        statement = getConnection().prepareStatement("SELECT * FROM logi");
                        break;
                    default:
                        statement = getConnection().prepareStatement("err");
                        break;
                }

                openNewWindow(statement.executeQuery());
                connection.commit();

            }catch (Exception e){
                connection.rollback();
                Alert alert = new Alert(Alert.AlertType.INFORMATION);
                alert.setTitle("Błąd");
                alert.setHeaderText(e.getMessage());
                alert.showAndWait().ifPresent(rs -> {
                    if (rs == ButtonType.OK) { }
                });
            }finally {
                connection.setAutoCommit(true); // Rozpocznij transakcję
            }

        }catch (Exception e){
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setTitle("Błąd połączenia");
            alert.setHeaderText(e.getMessage());
            alert.showAndWait().ifPresent(rs -> {
                if (rs == ButtonType.OK) { }
            });
        }




    }

    private int countParameters(String query) {
        int count = 0;
        for (char c : query.toCharArray()) {
            if (c == '?') {
                count++;
            }
        }
        return count;
    }

    private void openNewWindow(ResultSet resultSet) {
        try {

            FXMLLoader loader = new FXMLLoader(getClass().getResource("ResultsWindow.fxml"));
            Parent root = loader.load();


            Stage newWindow = new Stage();
            newWindow.setTitle("Wynik");
            newWindow.setScene(new Scene(root));

            ResultsWindowController controller = loader.getController();
            controller.printTable(resultSet);

            newWindow.show();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
