import javafx.fxml.FXML;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

import java.util.Random;

/**
 * Kontroler dla dla okna z samą kratą z komórkami
 * Obsługuje generowanie i wyświetlanie siatki
 */
public class GridWindowController {

    static int m;
    static int n;
    int k;
    double p;

    /**
     * Generator pseudolosowhy
     */
    static Random random = new Random();
    /**
     * Lista wszystkich komórek
     */
    static Cell[][] cells;
    /**
     * Grid Pane w którym będą przechowywane komórki
     */
    GridPane ColorGridPane;

    @FXML
    private AnchorPane anchorPane;

    /**
     * Generuje siatkę prostokątów o losowych kolorach i dodaje je do GridPane.
     * Każdy prostokąt jest powiązany z obiektem Cell gdzie są obsługiwane poszczególne pola siatki
     */
    public void GenerateGrid(){
        cells = new Cell[m][n];
        ColorGridPane = new GridPane();
        ColorGridPane.setLayoutX(0);
        ColorGridPane.setLayoutY(0);
        anchorPane.getChildren().add(ColorGridPane);
        for(int y = 0;y < n;y++){
            for(int x = 0;x < m;x++){
                Rectangle rect = new Rectangle();
                int red = random.nextInt(256);
                int green = random.nextInt(256);
                int blue = random.nextInt(256);

                rect.setFill(Color.rgb(red,green,blue));
                rect.setWidth(20);
                rect.setHeight(20);
                cells[x][y] = new Cell(rect,k,p,x,y);
                ColorGridPane.add(rect,x,y);
            }
        }
    }

}
