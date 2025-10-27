import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Point2D;
import javafx.scene.Group;
import javafx.scene.control.*;
import javafx.scene.shape.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;
import java.util.Scanner;

/**
 * Kontroler głownego okna programu
 */
public class FiguryPaintController implements Initializable {

    /**
     * typ kształtu wybrany do namalowania
     */
    String chosenShapeToDraw = "";
    /**
     * zmienna określająca czy użytkownik wybrał jeden z trzech przycisków rysujących kształty
     */
    boolean areWeDrawing = false;
    /**
     * zmienna określająca czy użytkownik wybrał przyciska odpowiadający za operacje na kształcie
     */
    static boolean areWeMoving = false;
    /**
     * Lista wszystkich stworzonych figur
     */
    ArrayList<Shape> DrawnShapesList = new ArrayList<Shape>();
    /**
     * Aktywny kształt
     */
    static Shape chosenShapeToMove;
    /**
     * Punkty wybrane myszką urzywane do stworzenia wybranej figury
     */
    Point2D[] PickedPoints = new Point2D[3];
    @FXML
    private Label SaveLoadLabel;
    @FXML
    private Group RotateGroup;
    @FXML
    private Group ColorGroup;
    @FXML
    private Slider RotateSlider;
    @FXML
    private Label OutputLabel;
    @FXML
    private ColorPicker ColorPicker;
    @FXML
    private Pane PaintPane;
    @FXML
    private Line PreviewLine;
    @FXML
    private Circle PreviewCircle;
    @FXML
    private Rectangle PreviewRectangle;
    @FXML
    private Polygon PreviewTriangle;
    /**
     * Podczas inicjalizacji dodajemu metody do obsługi slidera odpowiadającego za obrót figur
     * oraz do colorPickera odpowiadajacego za możliwość zmiany koloru. Dodatkowo dodajemy clip
     * do planszy oraz przypisujemy metody odpowiadające za kliknięcie lmb i rmb oraz przeciąganie myszy
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        PaintPane.setClip(new Rectangle(PaintPane.getPrefWidth(),PaintPane.getPrefHeight()));

        PaintPane.setOnMouseClicked(event -> {
            switch (event.getButton()) {
                case PRIMARY -> PRIMARYClicked(event);
                case SECONDARY -> SECONDARYClicked();
            }
        });

        PaintPane.setOnMouseMoved(event -> PRIMARYDrag(event));

        RotateSlider.valueProperty().addListener((observable, oldValue, newValue) -> chosenShapeToMove.setRotate(newValue.doubleValue() * 360d));

        ColorPicker.valueProperty().addListener((observable, oldValue, newValue) -> {
            chosenShapeToMove.setFill(newValue);
            ColorGroup.setVisible(false);
        });
    }

    /**
     * Funkcja wykonująca się gdy zostanie wciśnięty lmb na panelu, odpowiada za rysowanie wybranego kształtu,
     * dodaje każde kliknięcie do tablicy, gdy zostanie zapisana odpowiednia ilość punktów (2 lub 3 w zależności od kształtu)
     * zostaje narysowany kształt a tablica wyczyszczona.
     * @param e Przekazany event z kliknięcia
     */
    public void PRIMARYClicked(MouseEvent e){
        ColorGroup.setVisible(false);
        if(areWeDrawing){
            if( PickedPoints[0] == null ) { PickedPoints[0] = new Point2D(e.getX(),e.getY()); }
            else if ( PickedPoints[1] == null ) { PickedPoints[1] = new Point2D(e.getX(),e.getY()); }
            else if ( PickedPoints[2] == null ) { PickedPoints[2] = new Point2D(e.getX(),e.getY()); }
            Shape shape = null;
            switch (chosenShapeToDraw) {
                case "k":
                    shape = Drawing.DrawCircle(PickedPoints);
                    break;
                case "p":
                    shape = Drawing.DrawRectangle(PickedPoints);
                    break;
                case "t":
                    shape = Drawing.DrawTriangle(PickedPoints);
                    break;
            }
            if(shape != null){
                PaintPane.getChildren().add(shape);
                DrawnShapesList.add(shape);
                PickedPoints = new Point2D[3];
            }
        }
    }

    /**
     * Funkcja po wciśnięciu rmb pokazuje menu wyboru koloru aktywnej figury
     */
    public void SECONDARYClicked(){
        if(areWeMoving && chosenShapeToMove != null){
        ColorGroup.setVisible(true);
        ColorPicker.valueProperty().setValue((Color)chosenShapeToMove.getFill());
        }
    }

    /**
     * Funkcja odpowiada za rysowanie podglądów
     * @param e Przekazany event z kliknięcia
     */
    public void PRIMARYDrag(MouseEvent e){
        if(areWeDrawing){
            switch (chosenShapeToDraw){
                case "k":
                    if(PickedPoints[0] != null){
                        PreviewCircle.setVisible(true);
                        PreviewCircle.toFront();
                        PreviewCircle.setCenterX(PickedPoints[0].getX());
                        PreviewCircle.setCenterY(PickedPoints[0].getY());
                        PreviewCircle.setRadius(PickedPoints[0].distance(e.getX(),e.getY()));
                    }else {
                        PreviewCircle.setVisible(false);
                    }
                    break;
                case "p":
                    if(PickedPoints[0] != null){
                        PreviewRectangle.setVisible(true);
                        PreviewRectangle.toFront();
                        if(PickedPoints[0].getX() < e.getX()){
                            PreviewRectangle.setX(PickedPoints[0].getX());
                            PreviewRectangle.setWidth(e.getX() - PickedPoints[0].getX() );
                        }else{
                            PreviewRectangle.setX(e.getX());
                            PreviewRectangle.setWidth(PickedPoints[0].getX() - e.getX());
                        }
                        if(PickedPoints[0].getY() < e.getY()){
                            PreviewRectangle.setY(PickedPoints[0].getY());
                            PreviewRectangle.setHeight(e.getY() - PickedPoints[0].getY() );
                        }else{
                            PreviewRectangle.setY(e.getY());
                            PreviewRectangle.setHeight(PickedPoints[0].getY() - e.getY());
                        }
                    }else {
                        PreviewRectangle.setVisible(false);
                    }
                    break;
                case "t":
                    if(PickedPoints[0] != null && PickedPoints[1] == null){
                        PreviewLine.setVisible(true);
                        PreviewLine.toFront();
                        PreviewLine.setStartX(PickedPoints[0].getX());
                        PreviewLine.setStartY(PickedPoints[0].getY());
                        PreviewLine.setEndX(e.getX());
                        PreviewLine.setEndY(e.getY());
                    }else if(PickedPoints[1] != null ) {
                        PreviewLine.setVisible(false);
                        PreviewTriangle.setVisible(true);
                        PreviewTriangle.toFront();
                        PreviewTriangle.getPoints().set(0,PickedPoints[0].getX());
                        PreviewTriangle.getPoints().set(1,PickedPoints[0].getY());
                        PreviewTriangle.getPoints().set(2,PickedPoints[1].getX());
                        PreviewTriangle.getPoints().set(3,PickedPoints[1].getY());
                        PreviewTriangle.getPoints().set(4,e.getX());
                        PreviewTriangle.getPoints().set(5,e.getY());
                    }else{
                        PreviewTriangle.setVisible(false);
                    }
                    break;
            }
        }
    }

    /**
     * Funkcja odpowiada za aktywacje kształtu
     * @param shape Aktywowany kształt
     */
    public static void SelectShape(Shape shape){
        if(areWeMoving){
            if(chosenShapeToMove != null){
                chosenShapeToMove.setStroke(Color.BLACK);
            }
            chosenShapeToMove = shape;
            chosenShapeToMove.setStroke(Color.RED);
        }
    }

    /**
     * Funkcja ustawia wszystkie zmienne do wartośći domyślnych
     */
    public void SetEverythingToDefault(){
        areWeDrawing = false;
        areWeMoving = false;
        chosenShapeToDraw = null;
        if(chosenShapeToMove != null){
            chosenShapeToMove.setStroke(Color.BLACK);
            chosenShapeToMove = null;
        }
        RotateGroup.setVisible(false);
        PreviewLine.setVisible(false);
        PreviewCircle.setVisible(false);
        PreviewRectangle.setVisible(false);
        PreviewTriangle.setVisible(false);
    }

    /**
     * Funkcja jest wykonywana gdy wciśnięty zostaje przycisk z kołem, ustawia wybrany kształt jako koło,
     * zaznacza że użytkownik wybrał opcje rysowania i odznacza wybóe opjci manipulacji kształtem,
     * do tego chowa menu obrotu figurą i deaktywuje aktywną figurę
     */
    public void CircButtonClicked(){
        SetEverythingToDefault();
        chosenShapeToDraw = "k";
        areWeDrawing = true;
        OutputLabel.setText("Wybrano: Koło");
    }

    /**
     * Funkcja jest wykonywana gdy wciśnięty zostaje przycisk z prostokątem, ustawia wybrany kształt jako prostokąt,
     * zaznacza że użytkownik wybrał opcje rysowania i odznacza wybóe opjci manipulacji kształtem,
     * do tego chowa menu obrotu figurą i deaktywuje aktywną figurę
     */
    public void RectButtonClicked(){
        SetEverythingToDefault();
        chosenShapeToDraw = "p";
        areWeDrawing = true;
        OutputLabel.setText("Wybrano: Prostokąt");
    }

    /**
     * Funkcja jest wykonywana gdy wciśnięty zostaje przycisk z trókątem, ustawia wybrany kształt jako trójkąt,
     * zaznacza że użytkownik wybrał opcje rysowania i odznacza wybóe opjci manipulacji kształtem,
     * do tego chowa menu obrotu figurą i deaktywuje aktywną figurę
     */
    public void TriButtonClicked(){
        SetEverythingToDefault();
        chosenShapeToDraw = "t";
        areWeDrawing = true;
        OutputLabel.setText("Wybrano: Trójkąt");
    }

    /**
     * Funkcja jest wykonywana gdy wciśnięty zostaje przycisk z M, zaznacz że urzytkownik wybrał opcję manipulacji figurą
     * i odznacza wybór rysowania oraz pokazuje menu obrotu figurą
     */
    public void MoveButtonClicked(){
        SetEverythingToDefault();
        areWeMoving = true;
        RotateGroup.setVisible(true);
        OutputLabel.setText("Wybrano: Poruszanie");
    }

    /**
     * Funkcja zapisuje do pliku o nazwie ZapisanaPlansza aktualną zawartość planszy z figurami
     */
    public void SaveButtonClicked(){

        try{
            new java.io.File("ZapisanaPlansza").delete();
            SaveLoadLabel.setText("Zapisano tablice");
            FileWriter writer = new FileWriter("ZapisanaPlansza");
            int id = 0;
            String string = "";
            for(Shape shape : DrawnShapesList){
                string += "ID=" +id+ "\n";id++;
                string += shape.getClass().getSimpleName() +"\n";
                switch (shape.getClass().getSimpleName()){
                    case "Circle":
                        Circle circle = (Circle)shape;
                        //Srodek
                        string += circle.getCenterX() + "\n";
                        string += circle.getCenterY() + "\n";
                        //Promien
                        string += circle.getRadius() + "\n";
                        //Skala
                        string += circle.getScaleX() + "\n";
                        string += circle.getScaleY() + "\n";
                        //Rotacja
                        string += circle.getRotate() + "\n";
                        //Trasnlacje
                        string += circle.getTranslateX() + "\n";
                        string += circle.getTranslateY() + "\n";
                        //Kolor
                        string += circle.getFill().toString() + "\n";
                        break;
                    case "Rectangle":
                        Rectangle rect = (Rectangle) shape;
                        //Wymiary
                        string += rect.getWidth() + "\n";
                        string += rect.getHeight()  + "\n";
                        //Lokalizacja
                        string += rect.getX() + "\n";
                        string += rect.getY() + "\n";
                        //Skala
                        string += rect.getScaleX() + "\n";
                        string += rect.getScaleY() + "\n";
                        //Rotacja
                        string += rect.getRotate() + "\n";
                        //Trasnlacje
                        string += rect.getTranslateX() + "\n";
                        string += rect.getTranslateY() + "\n";
                        //Kolor
                        string += rect.getFill().toString() + "\n";
                        break;
                    case "Polygon":
                        Polygon tri = (Polygon) shape;
                        //Pierwszy punkt
                        string += tri.getPoints().get(0)  + "\n";
                        string += tri.getPoints().get(1)  + "\n";
                        //Drugi punkt
                        string += tri.getPoints().get(2)  + "\n";
                        string += tri.getPoints().get(3)  + "\n";
                        //Trzeci punkt
                        string += tri.getPoints().get(4)  + "\n";
                        string += tri.getPoints().get(5)  + "\n";
                        //Skala
                        string += tri.getScaleX() + "\n";
                        string += tri.getScaleY() + "\n";
                        //Rotacja
                        string += tri.getRotate() + "\n";
                        //Trasnlacje
                        string += tri.getTranslateX() + "\n";
                        string += tri.getTranslateY() + "\n";
                        //Kolor
                        string += tri.getFill().toString() + "\n";
                        break;
                }
            }
            writer.write(string);
            writer.close();
        }catch(IOException e) {
            System.out.println("Wystąpił błąd podczas zapisu do pliku: " + e.getMessage());
            SaveLoadLabel.setText("Wystąpił błąd przy zapisaniu tablicy");
        }
    }

    /**
     * Funkcja wczytuje z pliku o nazwie ZapisanaPlansza figury i dodaje je do planszy z figurami
     */
    public void LoadButtonClicked(){
        StringBuilder sb = new StringBuilder();
        try {

            for(Shape shape : DrawnShapesList){
                PaintPane.getChildren().remove(shape);
            }
            DrawnShapesList = new ArrayList<Shape>();

            SaveLoadLabel.setText("Wczytano tablice");
            FileReader reader = new FileReader("ZapisanaPlansza");
            int i;
            while ((i = reader.read()) != -1) {
                sb.append((char) i);
            }
            reader.close();

            Scanner scanner = new Scanner(sb.toString());

            while(scanner.hasNextLine()){
                String line = scanner.nextLine();
                if(line.matches("ID=.*")){
                    switch (scanner.nextLine()){
                        case "Circle":
                            //Srodek
                            double centerX = Double.parseDouble(scanner.nextLine());
                            double centerY = Double.parseDouble(scanner.nextLine());
                            //Promien
                            double radious = Double.parseDouble(scanner.nextLine());
                            //Stwórz kształt
                            Circle circle = Drawing.DrawCircle(new Point2D[]{new Point2D(centerX,centerY),
                                                                             new Point2D(centerX + radious,centerY)});
                            //Skala
                            circle.setScaleX(Double.parseDouble(scanner.nextLine()));
                            circle.setScaleY(Double.parseDouble(scanner.nextLine()));
                            //Rotacja
                            circle.setRotate(Double.parseDouble(scanner.nextLine()));
                            //Trasnlacje
                            circle.setTranslateX(Double.parseDouble(scanner.nextLine()));
                            circle.setTranslateY(Double.parseDouble(scanner.nextLine()));
                            //Kolor
                            circle.setFill(Color.valueOf(scanner.nextLine()));
                            //inne
                            circle.setStroke(Color.BLACK);
                            circle.setStrokeWidth(3);
                            //
                            PaintPane.getChildren().add(circle);
                            DrawnShapesList.add(circle);
                            break;
                        case "Rectangle":
                            //Wymiary
                            double Width =  Double.parseDouble(scanner.nextLine());
                            double Height =  Double.parseDouble(scanner.nextLine());
                            //Lokalizacja
                            double X =  Double.parseDouble(scanner.nextLine());
                            double Y =  Double.parseDouble(scanner.nextLine());
                            //Stwórz kształt
                            Rectangle rect = Drawing.DrawRectangle(new Point2D[]{new Point2D(X,Y),
                                                                   new Point2D(X + Width,Y+Height)});
                            //Skala
                            rect.setScaleX(Double.parseDouble(scanner.nextLine()));
                            rect.setScaleY(Double.parseDouble(scanner.nextLine()));
                            //Rotacja
                            rect.setRotate(Double.parseDouble(scanner.nextLine()));
                            //Trasnlacje
                            rect.setTranslateX(Double.parseDouble(scanner.nextLine()));
                            rect.setTranslateY(Double.parseDouble(scanner.nextLine()));
                            //Kolor
                            rect.setFill(Color.valueOf(scanner.nextLine()));
                            //inne
                            rect.setStroke(Color.BLACK);
                            rect.setStrokeWidth(3);
                            //
                            PaintPane.getChildren().add(rect);
                            DrawnShapesList.add(rect);
                            break;
                        case "Polygon":
                            //Pierwszy punkt
                            double X1 =  Double.parseDouble(scanner.nextLine());
                            double Y1 =  Double.parseDouble(scanner.nextLine());
                            //Drugi punkt
                            double X2 =  Double.parseDouble(scanner.nextLine());
                            double Y2 =  Double.parseDouble(scanner.nextLine());
                            //Trzeci punkt
                            double X3 =  Double.parseDouble(scanner.nextLine());
                            double Y3 =  Double.parseDouble(scanner.nextLine());
                            //Stwórz kształt
                            Polygon tri = Drawing.DrawTriangle(new Point2D[]{new Point2D(X1,Y1),
                                                                                new Point2D(X2,Y2),
                                                                                new Point2D(X3,Y3)});
                            //Skala
                            tri.setScaleX(Double.parseDouble(scanner.nextLine()));
                            tri.setScaleY(Double.parseDouble(scanner.nextLine()));
                            //Rotacja
                            tri.setRotate(Double.parseDouble(scanner.nextLine()));
                            //Trasnlacje
                            tri.setTranslateX(Double.parseDouble(scanner.nextLine()));
                            tri.setTranslateY(Double.parseDouble(scanner.nextLine()));
                            //Kolor
                            tri.setFill(Color.valueOf(scanner.nextLine()));
                            //inne
                            tri.setStroke(Color.BLACK);
                            tri.setStrokeWidth(3);
                            //
                            PaintPane.getChildren().add(tri);
                            DrawnShapesList.add(tri);
                    }
                }
            }



        } catch (IOException e) {
            System.out.println("Wystąpił błąd podczas wczytywania pliku: " + e.getMessage());
            SaveLoadLabel.setText("Wystąpił błąd przy wczytwyaniu tablicy");
        }

    }

    /**
     * Funkcja wyświetla informacje o projekcie i instrukcje jego obsługi
     */
    public void InfoButonClicked(){
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Informacja");
        alert.setHeaderText(null);
        alert.setContentText("Nazwa: Figury Paint \n" +
                                "Autor: Jan Brzoska \n"+
                                "Nazwa: FiguryPaint \n" +
                                "Przeznaczenie: Aplikacja pozwala rysować koła, prostokąty i trójkąty. Można przemieszczać figury, obracać, skalować" +
                                " oraz zmieniać kolor wypełnienia. Jest też opcja zapisu do pliku i wczytania z niego \n" +
                                "Instrukcja:\n"+
                                "1. Przycisk z kwadratem: dwa następne kliknięcia lewym przyciskiem myszy na plansze wyznaczą wyznaczą prostokąt oparty na tych punktach\n"+
                                "2. Przycisk z kołem: dwa następne kliknięcia lewym przyciskiem myszy na plansze wyznaczą środek i promień kołą i je stworzą \n"+
                                "3. Przycisk z trojkątem: trzy następne kliknięcia lewym przyciskiem myszy na plansze wyznaczą trojkąt oparty na tych punktach\n" +
                                "4. Przycisk z M: po wciśnięciu tego przycisku można, aktywować figurę lewym przyciskiem myszy, poruszanie aktywowanej figury myszą,\n" +
                                "skalowanie jej scrollem oraz obracanie jej za pomocą pojawiającego się slidera,\n " +
                                "po wciśnięciu prawego przycisku myszy na figurze pojawi się menu wybrania koloru\n" +
                                "5. Przycisk Zapisz: Zapisuje planszę do pliku ZapisanaPlansza\n"+
                                "6. Przycisk Wczytaj: Wczytuje wcześniej zapisaną planszę");
        alert.getDialogPane().setPrefWidth(600);
        alert.getDialogPane().setPrefHeight(400);
        alert.showAndWait();
    }
}