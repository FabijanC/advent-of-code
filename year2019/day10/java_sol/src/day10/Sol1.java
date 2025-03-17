package day10;

import java.io.FileNotFoundException;
import java.util.List;

import day10.Util.Asteroid;
import day10.Util.DirectedLine;

public class Sol1 {

    public static void main(String[] args) throws FileNotFoundException {
        List<Asteroid> asteroids = Util.getAsteroidsFromFile(args[0]);
        
        int maxi = 0;   
        Asteroid sol = null;
        for (Asteroid a1: asteroids) {
            int cnt = 0;
            for (Asteroid a2: asteroids) {
                if (a1 == a2) {
                    continue;
                }
                DirectedLine line = new DirectedLine(a1, a2);
                boolean visible = true;
                for (Asteroid other: asteroids) {
                    if (other == a1 || other == a2) {
                        continue;
                    }
                    
                    if (line.contains(other)) {
                        visible = false;
                        break;
                    }
                }
                
                if (visible) {
                    ++cnt;
                }
            }
            
            if (cnt > maxi) {
                sol = a1;
                maxi = cnt;
            }
        }

        System.out.println(sol + " " + maxi);
    }
}