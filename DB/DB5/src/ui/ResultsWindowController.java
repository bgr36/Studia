package ui;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;

import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.List;


public class ResultsWindowController {

    @FXML
    private TableView<ObservableList<String>> resultsTable;

    public void setTextArea(String s){

    }

    public void printTable(ResultSet resultSet){

        try{

            ObservableList<ObservableList<String>> data = FXCollections.observableArrayList();
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();

            // Utwórz kolumny w TableView dynamicznie
            List<TableColumn<ObservableList<String>, String>> columns = new ArrayList<>();
            for (int i = 1; i <= columnCount; i++) {
                final int columnIndex = i;
                TableColumn<ObservableList<String>, String> column = new TableColumn<>(metaData.getColumnName(i));
                column.setCellValueFactory(cellData -> {
                    String value = cellData.getValue().get(columnIndex - 1);
                    return new javafx.beans.property.SimpleStringProperty(value);
                });
                columns.add(column);
            }

            // Dodaj kolumny do TableView
            resultsTable.getColumns().setAll(columns);

            // Wczytaj dane z ResultSet do ObservableList
            while (resultSet.next()) {
                ObservableList<String> row = FXCollections.observableArrayList();
                for (int i = 1; i <= columnCount; i++) {
                    row.add(resultSet.getString(i));
                }
                data.add(row);
            }

            // Przypisz dane do TableView
            resultsTable.setItems(data);

        }catch (Exception e){
            e.printStackTrace();
        }

    }

}
