import org.apache.commons.math3.random.MersenneTwister;
import org.apache.commons.math3.random.RandomGenerator;

import java.util.Arrays;
import java.util.function.Function;


public class MainOld {

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

    static void case1(int k, double left, double right, double up, Function<Double,Double> f){

         for(int i = 50;i < 5001 ;i += 50) {
             double[] results = new double[k];
             System.out.println("Dla n = " + i);
             for(int j = 0;j < k;j++){
                 int C = 0;
                 System.out.println("    k = " + (j+1));
                 for(int l = 0;l < i;l++){
                    double pointx = left + (right - left) * mt.nextDouble();
                    double pointy = up * mt.nextDouble();
                    boolean contains = pointy <= f.apply(pointx);
                    if(contains) {C++;}
                    System.out.println("     x = " + pointx + " y = " + pointy + " " + contains );
                 }
                 results[j] = (double)C/i * (right - left) * up;
             }
             System.out.println("Szacowany wynik całki dla n = " + i + " to " + Arrays.stream(results).average().orElse(0.0));
         }
    }

    public static void main(String[] args) {
        case1(20,0,1,0.5, MainOld::f3);
    }
}