import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Klasa reprezentująca pojedynczą komórkę w siatce
 */
public class Cell  {
    /**
     * Zmienna oznaczająca czy komórka jest aktywna
     */
    AtomicBoolean running = new AtomicBoolean(true);

    /**
     * Prostokąt reprezentujący graficzną część komórki
     */
    private Rectangle rect;


    private int y;
    private int x;
    private int k;
    private double p;

    /**
     * Tworzy nową komórkę.
     *
     * @param Rect Prostokąt reprezentujący komórkę
     * @param K Prędkość działania
     * @param P Prawdopodobieństwo losowej zmiany koloru
     * @param M Pozycja komórki w siatce (x)
     * @param N Pozycja komórki w siatce (y)
     */
    public Cell(Rectangle Rect, int K, double P, int M, int N) {
        x = M;
        y = N;
        rect = Rect;
        k = K;
        p = P;

        rect.setOnMouseClicked(mouseEvent -> running.set(!running.get()));

        thread.setDaemon(true);
        thread.start();
    }

    /**
     * Wątek odpowiedzialny za zmianę koloru komórki.
     */
    Thread thread = new Thread(() -> {
        while (true) {
            if (running.get()) {
                try {
                    int delay = (int) (GridWindowController.random.nextDouble(0.5, 1.5) * k);
                    Thread.sleep(delay);

                    synchronized (GridWindowController.cells) {
                        System.out.println("Start: " + Thread.currentThread().threadId());
                        if (GridWindowController.random.nextDouble() <= p) {
                            javafx.application.Platform.runLater(() -> rect.setFill(Color.rgb(
                                    (int) (Math.random() * 255),
                                    (int) (Math.random() * 255),
                                    (int) (Math.random() * 255)
                            )));
                        } else {
                            javafx.application.Platform.runLater(() -> rect.setFill(AddColors()));
                        }
                        System.out.println("End: " + Thread.currentThread().threadId());
                    }

                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    });

    /**
     * Oblicza i zwraca średni kolor sąsiednich komórek które są aktywne.
     */
    Color AddColors() {
        Color leftColor = Color.rgb(0, 0, 0);
        Color rightColor = Color.rgb(0, 0, 0);
        Color upColor = Color.rgb(0, 0, 0);
        Color downColor = Color.rgb(0, 0, 0);
        int count = 0;

        if (GridWindowController.cells[(x - 1 + GridWindowController.m) % GridWindowController.m][y].running.get()) {
            leftColor = (Color) GridWindowController.cells[(x - 1 + GridWindowController.m) % GridWindowController.m][y].rect.getFill();
            count++;
        }

        if (GridWindowController.cells[(x + 1) % GridWindowController.m][y].running.get()) {
            rightColor = (Color) GridWindowController.cells[(x + 1) % GridWindowController.m][y].rect.getFill();
            count++;
        }

        if (GridWindowController.cells[x][(y - 1 + GridWindowController.n) % GridWindowController.n].running.get()) {
            upColor = (Color) GridWindowController.cells[x][(y - 1 + GridWindowController.n) % GridWindowController.n].rect.getFill();
            count++;
        }

        if (GridWindowController.cells[x][(y + 1) % GridWindowController.n].running.get()) {
            downColor = (Color) GridWindowController.cells[x][(y + 1) % GridWindowController.n].rect.getFill();
            count++;
        }

        return Color.rgb(
                (int) ((upColor.getRed() + downColor.getRed() + rightColor.getRed() + leftColor.getRed()) * 255 / count),
                (int) ((upColor.getGreen() + downColor.getGreen() + rightColor.getGreen() + leftColor.getGreen()) * 255 / count),
                (int) ((upColor.getBlue() + downColor.getBlue() + rightColor.getBlue() + leftColor.getBlue()) * 255 / count));
    }
}
