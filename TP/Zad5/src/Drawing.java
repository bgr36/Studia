import javafx.geometry.Point2D;
import javafx.scene.input.MouseButton;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Polygon;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;

/**
 *Klasa zawiera funkcje rysujące poszczególne kształty
 */
public class Drawing {

    /**
     * zmienne przechowujące tymczasowe współrzędne kursora
     */
    static double mouseX,mouseY;

    /**
     * Funkcja dodaje do podanego kształtu a odpowiednie eventy by dało się go edytować
     * @param a kształ któremu dodajemy funkcje
     */
    static void AddFunctions(Shape a){

        //Na kliknięcie myszą wysuwany figurę na przód, zbieramy jej pozycje potrzebną do poźniejszego przesuwania oraz aktywyjemy figurę
        a.setOnMousePressed(event -> {
            if(event.getButton() == MouseButton.PRIMARY){
                a.toFront();
                mouseX = event.getSceneX();
                mouseY = event.getSceneY();
                FiguryPaintController.SelectShape(a);
            }
        });

        //Gdy przesuwamy figurę podąrza za kursowem, na początku przesuwamy na zapisane koordynaty z setOnMousePressed potem za każdym wykonanym ruchem zapisujemy nowe na które się przesuniemy
        a.setOnMouseDragged(event -> {
            if( FiguryPaintController.areWeMoving && FiguryPaintController.chosenShapeToMove == a && event.getButton() == MouseButton.PRIMARY){
                a.setTranslateX(a.getTranslateX() + event.getSceneX() - mouseX);
                a.setTranslateY(a.getTranslateY() + event.getSceneY() - mouseY);

                mouseX = event.getSceneX();
                mouseY = event.getSceneY();
            }
        });

        //Przy scrolowaniu na zaznaczonej figurze zmieniamy jej skale
        a.setOnScroll(event -> {
            if( FiguryPaintController.areWeMoving && FiguryPaintController.chosenShapeToMove == a){
                double scale = event.getDeltaY() > 0 ? 1.1 : 0.9;
                a.setScaleX(a.getScaleX() * scale);
                a.setScaleY(a.getScaleY() * scale);
            }
        });

    }

    /**
     * Funkcja rysująca koło oraz przypisująca kształtowi poszczególne operacje na nim
     * @param points Pierwszy element to środek koła, drugi wyznacza promień
     * @return Figura z przypisanymi funkcjami modyfikacji
     */
    public static Circle DrawCircle(Point2D[] points){
        if(points[0] != null && points[1] != null){
            Circle circle = new Circle(points[0].distance(points[1]));
            circle.setCenterX(points[0].getX());
            circle.setCenterY(points[0].getY());
            circle.setStroke(Color.BLACK);
            circle.setStrokeWidth(3);
            circle.setFill(Color.rgb(244,244,244,1));

            AddFunctions(circle);

            return circle;
        }else {
            return null;
        }

    }


    /**
     * Funkcja rysująca prostokąt oraz przypisująca kształtowi poszczególne operacje na nim
     * @param points Punkt pierwszy i punkt drugi leża na tej samej przekątnej prostokąta, na ich podstawie tworzy się kształt
     * @return Figura z przypisanymi funkcjami modyfikacji
     */
    public static Rectangle DrawRectangle(Point2D[] points){
        if(points[0] != null && points[1] != null ){
            Rectangle rect = new Rectangle((Math.abs(points[0].getX() - points[1].getX())),
                                           (Math.abs(points[0].getY() - points[1].getY())));
            rect.setX(Math.min(Math.abs(points[0].getX()),Math.abs(points[1].getX())));
            rect.setY(Math.min(Math.abs(points[0].getY()),Math.abs(points[1].getY())));
            rect.setStroke(Color.BLACK);
            rect.setStrokeWidth(3);
            rect.setFill(Color.rgb(244,244,244,1));

            AddFunctions(rect);

            return rect;
        }else {
            return null;
        }
    }


    /**
     * Funkcja rysująca prostokąt oraz przypisująca kształtowi poszczególne operacje na nim
     * @param points Kolejne trzy punkty to kolejne wierzchołki trójkąta
     * @return Figura z przypisanymi funkcjami modyfikacji
     */
    public static Polygon DrawTriangle(Point2D[] points){
        if(points[0] != null && points[1] != null && points[2] != null ){
            Polygon tri = new Polygon(points[0].getX(),points[0].getY(),
                    points[1].getX(),points[1].getY(),
                    points[2].getX(),points[2].getY());
            tri.setStroke(Color.BLACK);
            tri.setStrokeWidth(3);
            tri.setFill(Color.rgb(244,244,244,1));

            AddFunctions(tri);

            return tri;
        }else {
            return null;
        }
    }

}
