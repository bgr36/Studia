import java.util.Random;
import java.util.ArrayList;

//Sygnał 2x+1 długość tablicy
//Cel - każda stacja chce wysłać jeden sygnał.

public class HelloWorld {

    ArrayList<Signal> Signals = new ArrayList<Signal>();
    ArrayList<Station> Stations = new ArrayList<Station>();
    Random rand = new Random();
    static int globalID = 0;
    int[] finishedSignals = {0,0,0};
    int minDealy = 8;
    int maxDealy = 16;
    int turns = 0;
    int SignalLength = 20;
    int finished = 0;
    int[] stationsPos = {0, 11, 22};
    char[] stationsSym = {'A', 'B', 'C'};

    char isThiSpotTaken(int place){
        for (Signal s : Signals) {
            for (int i : s.signalPositions){
                if(i == place) { return s.symbol;}
            }
        }
        return 'O';
    }

    private class Signal {
        public char symbol;
        public int[] signalPositions = new int[SignalLength];
        int goalDestination;
        int direction; //1 right; -1 left;
        int ID = 0;

        public Signal(int startingPos, int direction, int goalDestination, char symbol) {
            this.symbol = symbol;
            this.direction = direction;
            this.goalDestination = goalDestination;
            signalPositions = new int[SignalLength];
            for (int i = 0; i < SignalLength - 1; i++) {
                signalPositions[i] = -10;
            }
            signalPositions[SignalLength - 1] = startingPos;
            ID = globalID++;
            //System.out.println("Spawned Signal:" + ID + " content:"+ symbol + " ["+signalPositions[0]+"] ["+signalPositions[1]+"] ["+signalPositions[2]+"]");
        }

        public int moveSignal() {
            // Sprawdź czy czoło sygnału dotarło do celu
            if (signalPositions[SignalLength - 1] + direction == goalDestination) {
                // Usuwaj kolejne segmenty sygnału (od początku)
                for (int i = 0; i < SignalLength; i++) {
                    if (signalPositions[i] != -10) {
                        signalPositions[i] = -10;
                        break;
                    }
                }
            } else {
                // Przesuń sygnał w kierunku
                for (int i = 0; i < SignalLength - 1; i++) {
                    signalPositions[i] = signalPositions[i + 1];
                }
                signalPositions[SignalLength - 1] = signalPositions[SignalLength - 1] + direction;
            }

            // Sprawdź czy sygnał się skończył
            boolean finished = true;
            for (int i = 0; i < SignalLength; i++) {
                if (signalPositions[i] != -10) {
                    finished = false;
                    break;
                }
            }
            if (finished) {
                switch (symbol) {
                    case 'a': finishedSignals[0]++; break;
                    case 'b': finishedSignals[1]++; break;
                    case 'c': finishedSignals[2]++; break;
                }
                return 1;
            } else {
                return 0;
            }

            
        }

        public void collided(){
            //System.out.println("Signal:" + ID + " content:"+ symbol + " collided");
            symbol = 'X';
        }

        public void destroy(){
            //System.out.println("Signal:" + ID + " content:"+ symbol + " destroyed");
            Signals.remove(this);
        }
        
    }

    private class Station {
        public int ID;
        int jammed = 0;
        int timesJammed = 0;
        public int waitTimer = 0;

        public Station(int ID) {
            this.ID = ID;
            waitTimer = rand.nextInt(12)+1;
        }

        public void makeTurn() {
            waitTimer--;
            jammed--;

            if(waitTimer < 0){
                checkForCollisions();
            }
            
            
            if(waitTimer < 0 && jammed < 0){
                if(checkIfFreeToTransmit()){
                makeSignal();
                waitTimer = rand.nextInt(maxDealy - minDealy + 1) + minDealy;}
            }
        }

        private void makeSignal() {
            int goal;
            int direction;
            if(rand.nextInt(2) == 0){
                goal = Math.floorMod((ID + 1),3);
            }else {goal = Math.floorMod((ID - 1),3);}

            if(goal > ID){
                direction = 1;
            }else {direction = -1;}
            
            Signal signal = new Signal(stationsPos[ID], direction, stationsPos[goal],  Character.toLowerCase(stationsSym[ID]));
            Signals.add(signal);
            
        }

        private boolean checkIfFreeToTransmit() {
            boolean free = true;
            char stationSymLowercase =  Character.toLowerCase(stationsSym[ID]);
            char left = isThiSpotTaken(stationsPos[ID]-1);
            char right = isThiSpotTaken(stationsPos[ID]+1);
            if((left != stationSymLowercase && left != 'O') || (right != stationSymLowercase && right != 'O')){
                free = false; 
            }
            return free;
        }

        private void checkForCollisions() {
            char left = isThiSpotTaken(stationsPos[ID]-1);
            char right = isThiSpotTaken(stationsPos[ID]+1);
            if(left == 'X' || right == 'X'){
                collisionDetected();
            } else if(left == 'J' || right == 'J'){
                jamDetected();
            }
        }

        private void collisionDetected() {
            jamDetected();

            int goal1 = Math.floorMod((ID - 1),3);
            int goal2 = Math.floorMod((ID + 1),3);
            int direction1;
            int direction2;

            if(goal1 > ID){
                direction1 = 1;
            }else {direction1 = -1;}

            if(goal2 > ID){
                direction2 = 1;
            }else {direction2 = -1;}

            Signal signal1 = new Signal(stationsPos[ID],direction1, stationsPos[goal1],  'J');
            Signals.add(signal1);
            
            Signal signal2 = new Signal(stationsPos[ID],direction2, stationsPos[goal2],  'J');
            Signals.add(signal2);            
        }

        private void jamDetected() {
            if(waitTimer < 0){
                timesJammed++;
                jammed = 4;
                waitTimer = timesJammed+1 * 4 ;
                //System.out.println("Station:" + stationsSym[ID] + " Jammed, waiting " + waitTimer + " turns");
            }
        }
    }

    void printBoard(){
        char[] toPrint = {'_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',};
        for (Signal s : Signals){
            if(isNormal(s)){
                for(int i : s.signalPositions){
                    if(i > -1){
                        toPrint[i] = s.symbol;
                    }
                }
            }
        }

        // for (Signal s : Signals){
        //     if(s.symbol == 'X'){
        //         for(int i : s.signalPositions){
        //             if(i > -1){
        //                 toPrint[i] = s.symbol;
        //             }
        //         }
        //     }
        // }

        for (Signal s : Signals){
            if(s.symbol == 'J'){
                for(int i : s.signalPositions){
                    if(i > -1){
                        toPrint[i] = s.symbol;
                    }
                }
            }
        }

        toPrint[stationsPos[0]] = stationsSym[0];
        toPrint[stationsPos[1]] = stationsSym[1];
        toPrint[stationsPos[2]] = stationsSym[2];
        System.out.print(turns + ". ");
        for(char c : toPrint) {
            System.out.print(c);
        }
        System.out.print("Recived signals: A:"+ finishedSignals[0]+" B:"+finishedSignals[1]+" C:"+finishedSignals[2]);
        System.out.print(" WaitTimes: A:"+ Stations.get(0).waitTimer +" B:"+Stations.get(1).waitTimer+" C:"+Stations.get(2).waitTimer);
        System.out.print("\n");
    }

    ArrayList<Signal> checkSignals() {
        ArrayList<Signal> signalsToDelete = new ArrayList<>();
        for (int i = 0; i < Signals.size(); i++) {
            Signal s1 = Signals.get(i);
            for (int j = 0; j < Signals.size(); j++) {
                if (i == j) continue;
                Signal s2 = Signals.get(j);

                for (int pos1 : s1.signalPositions) {
                    if (pos1 == -10) continue;
                    for (int pos2 : s2.signalPositions) {
                        if (pos2 == -10) continue;
                        if (pos1 == pos2) {
                            // Zwykły + zwykły
                            if (isNormal(s1) && isNormal(s2)) {
                                s1.collided();
                                s2.collided();
                            }
                            // Kolizja + zwykły
                            else if (s1.symbol == 'X' && isNormal(s2)) {
                                s2.collided();
                            }
                            else if (isNormal(s1) && s2.symbol == 'X') {
                                s1.collided();
                            }
                            // Jam + nie-Jam (zwykły lub kolizja)
                            else if (s1.symbol == 'J' && s2.symbol != 'J') {
                                if (!signalsToDelete.contains(s2)) signalsToDelete.add(s2);
                            }
                            else if (s2.symbol == 'J' && s1.symbol != 'J') {
                                if (!signalsToDelete.contains(s1)) signalsToDelete.add(s1);
                            }
                        }
                    }
                }
            }
        }
        return signalsToDelete;
    }

    // Pomocnicza metoda:
    private boolean isNormal(Signal s) {
        return s.symbol != 'J' && s.symbol != 'X';
    }

    public void runSimulation(int howLong) {
        Station A = new Station(0);
        Station B = new Station(1);
        Station C = new Station(2);
        Stations.add(A);
        Stations.add(B);
        Stations.add(C);

        while(finishedSignals[0]==0 || finishedSignals[1]==0 || finishedSignals[2]==0){

            ArrayList<Signal> SignalsToDelete = new ArrayList<Signal>();
            for(Signal s : Signals){
               int result = s.moveSignal();
               if(result == 1){SignalsToDelete.add(s);}
            }

            SignalsToDelete.addAll(checkSignals());

            for(Signal s : SignalsToDelete){
                s.destroy();
            }

            checkSignals();

            for(Station s : Stations){
                s.makeTurn();
            }

            printBoard();

            turns++;
        }


    }

    public static void main(String[] args) {
        HelloWorld simulation = new HelloWorld();
        simulation.runSimulation(200);
    }

}

