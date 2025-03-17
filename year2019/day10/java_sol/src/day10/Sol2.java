package day10;

import java.io.FileNotFoundException;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import day10.Util.Asteroid;

/**
 * LinkedList<Asteroid>
 * 
 * @author Fabijan
 *
 */
public class Sol2 {
	private static double getAngle(Asteroid a1, Asteroid pivot, Asteroid a2) {
		double angle =  Math.atan2(-a1.y + pivot.y, a1.x - pivot.x) - Math.atan2(-a2.y + pivot.y, a2.x - pivot.x);
		if (angle < 0) {
			angle = 2*Math.PI + angle;
		}
		return angle;
	}
	
	public static void main(String[] args) throws FileNotFoundException {
		List<Asteroid> asteroids = new LinkedList<>(Util.getAsteroidsFromFile(args[0]));
		
//		int x = 11;
//		int y = 13;
		int x = 37;
		int y = 25;
		Asteroid pivot = new Asteroid(x, y);
		Asteroid a0 = new Asteroid(x, 0);
		
//		System.out.println(getAngle(a0, pivot, new Asteroid(11, 0)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(20, 7)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(18, 10)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(20, 13)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(12, 10)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(12, 13)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(11, 20)));
//		
//		System.out.println(getAngle(a0, pivot, new Asteroid(10, 20)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(8, 15)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(8, 14)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(8, 13)));
//
//		System.out.println(getAngle(a0, pivot, new Asteroid(8, 11)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(8, 10)));
//		System.out.println();
//		
//		System.out.println(getAngle(a0, pivot, new Asteroid(11, 12)));
//		System.out.println(getAngle(a0, pivot, new Asteroid(12, 1)));
//		System.exit(1);
		
		asteroids.sort((a1, a2) -> {
			double angle1 = getAngle(a0, pivot, a1);
			double angle2 = getAngle(a0, pivot, a2);
			if (Math.abs(angle1 - angle2) < Util.EPS) {
				double dist1 = a1.getDistanceFrom(pivot);
				double dist2 = a2.getDistanceFrom(pivot);
				return Double.compare(dist1, dist2);
			}
			return Double.compare(angle1, angle2);
		});
		
		System.out.println(asteroids);
		
		Iterator<Asteroid> it = asteroids.iterator();
		Asteroid lastRemoved = it.next();
		it.remove();
		int cnt = 1;
		while (cnt < 200) {
			if (!it.hasNext()) {
				it = asteroids.iterator();
				continue;
			}
			
			Asteroid current = it.next();
			double angle = getAngle(lastRemoved, pivot, current);
			if (Math.abs(angle) < Util.EPS) {
				// pass
			} else {
				lastRemoved = current;
				System.out.println(lastRemoved);
				it.remove();
				++cnt;
			}
		}
		
		System.out.println(lastRemoved);
	}
}
