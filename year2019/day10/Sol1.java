import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.lang.Math;
import java.io.File;
import java.io.FileNotFoundException;

public class Sol1 {
    static final double EPS = 1e-6;
    
    static class Asteroid {
        final int x;
        final int y;
        Asteroid(int x, int y) {
            this.x = x;
            this.y = y;
        }
        
        double get_distance_from(Asteroid other) {
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
            this.length = a1.get_distance_from(a2);
        }
        
        boolean contains(Asteroid other) {
            double d1 = this.a1.get_distance_from(other);
            double d2 = this.a2.get_distance_from(other);
            return Math.abs(d1+d2 - this.length) < EPS;
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        List<String> lines = new ArrayList<>();
        File file = new File(args[0]);
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