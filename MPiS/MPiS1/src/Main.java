import org.apache.commons.math3.random.MersenneTwister;
import org.apache.commons.math3.random.RandomGenerator;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.function.Function;

public class Main {

    static RandomGenerator mt = new MersenneTwister(42);

    static double f1(double x){
        //3
        //0-8
        return Math.cbrt(x);
    }

    static double f2(double x){
        //1
        //0-pi
        return Math.sin(x);
    }

    static double f3(double x){
        //0.5
        //0-1
        return 4 * x * Math.pow(1-x,3);
    }

    static double pi(double x){
        //1
        //0-1
        return Math.sqrt(1 - x * x);
    }

    static void DoTest(int k, double left, double right, double up, Function<Double, Double> f, String filePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {

            writer.write("x ,");
            for (int i = 50; i <= 5000; i += 50) {
                writer.write(i + ",");
            }
            writer.write("\n");


            double[][] results = new double[k][(5000 / 50)];
            for (int j = 0; j < k; j++) {
                writer.write((j + 1) + ",");
                int colIndex = 0;
                for (int i = 50; i <= 5000; i += 50) {
                    int C = 0;
                    for (int l = 0; l < i; l++) {
                        double pointx = left + (right - left) * mt.nextDouble();
                        double pointy = up * mt.nextDouble();
                        if (pointy <= f.apply(pointx)) {
                            C++;
                        }
                    }
                    double result = (double) C / i * (right - left) * up;
                    results[j][colIndex++] = result;
                    writer.write(result + ",");
                }
                writer.write("\n");
            }


            writer.write("Avg,");
            for (int i = 0; i < results[0].length; i++) {
                double avg = 0;
                for (int j = 0; j < k; j++) {
                    avg += results[j][i];
                }
                avg /= k;
                writer.write(avg + ",");
            }
            writer.write("\n");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void DoTestDlaPi(int k, double left, double right, double up, Function<Double, Double> f, String filePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {

            writer.write("x ,");
            for (int i = 50; i <= 5000; i += 50) {
                writer.write(i + ",");
            }
            writer.write("\n");


            double[][] results = new double[k][(5000 / 50)];
            for (int j = 0; j < k; j++) {
                writer.write((j + 1) + ",");
                int colIndex = 0;
                for (int i = 50; i <= 5000; i += 50) {
                    int C = 0;
                    for (int l = 0; l < i; l++) {
                        double pointx = left + (right - left) * mt.nextDouble();
                        double pointy = up * mt.nextDouble();
                        if (pointy <= f.apply(pointx)) {
                            C++;
                        }
                    }
                    double result = ((double) C / i )* 4;
                    results[j][colIndex++] = result;
                    writer.write(result + ",");
                }
                writer.write("\n");
            }


            writer.write("Avg,");
            for (int i = 0; i < results[0].length; i++) {
                double avg = 0;
                for (int j = 0; j < k; j++) {
                    avg += results[j][i];
                }
                avg /= k;
                writer.write(avg + ",");
            }
            writer.write("\n");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String filePath = "wynikipik50.csv";
        //DoTest(50, 0, 1, 0.5, Main::f3, filePath);
        //DoTestDlaPi(50, 0, 1, 1, Main::pi, filePath);
    }
}