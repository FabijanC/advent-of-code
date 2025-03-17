package day10;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Util {
    static final double EPS = 1e-6;
    
    static class Asteroid {
        final int x;
        final int y;
        Asteroid(int x, int y) {
            this.x = x;
            this.y = y;
        }
        
        double getDistanceFrom(Asteroid other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return Math.sqrt(dx*dx + dy*dy);
        }
        
        @Override
        public boolean equals(Object o) {
            Asteroid other = (Asteroid) o;
            return this.x == other.x && this.x == other.y;
        }
        
        @Override
        public String toString() {
            return "A(" + this.x + "," + this.y + ")";
        }
    }

    static class DirectedLine {
        final Asteroid a1;
        final Asteroid a2;
        final double length;
        DirectedLine(Asteroid a1, Asteroid a2) {
            this.a1 = a1;
            this.a2 = a2;
            this.length = a1.getDistanceFrom(a2);
        }
        
        boolean contains(Asteroid other) {
            double d1 = this.a1.getDistanceFrom(other);
            double d2 = this.a2.getDistanceFrom(other);
            return Math.abs(d1+d2 - this.length) < EPS;
        }
    }
    
    public static List<Asteroid> getAsteroidsFromFile(String path) throws FileNotFoundException {
    	List<String> lines = new ArrayList<>();
        File file = new File(path);
        try (Scanner sc = new Scanner(file)) {
            while (sc.hasNext()) {
                lines.add(sc.nextLine());
            }
        }
        
        List<Asteroid> asteroids = new ArrayList<>();
        for (int y = 0; y < lines.size(); ++y) {
            String line = lines.get(y);
            for (int x = 0; x < line.length(); ++x) {
                if (line.charAt(x) == '#') {
                    asteroids.add(new Asteroid(x, y));
                }
            }
        }
        
        return asteroids;
    }
}
