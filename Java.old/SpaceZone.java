package izak.asteroids;

import java.awt.Color;
import java.awt.Graphics2D;
import java.util.ArrayList;
import java.util.Random;
import java.util.function.Predicate;

public class SpaceZone {

	private ArrayList<Asteroid[]> collidingAsteroidPairs;
	Ship playerShip;
	ArrayList<Asteroid> asteroids;
	ArrayList<Bullet> bullets;
	
	AsteroidsComponent asteroidsComponent;
	
	Random random;
	
	long lastFireTime = 0;
    int fireCooldown = 210; 
    boolean playerDead;
	
	public SpaceZone(AsteroidsComponent asteroidsComponentIn) {
		asteroidsComponent = asteroidsComponentIn;
		
		 random = new Random(2020);
		
		// use to load any assets
		collidingAsteroidPairs = new ArrayList<Asteroid[]>();
		
		bullets = new ArrayList<Bullet>();
		
		playerDead = false;
		playerShip = new Ship(asteroidsComponent.centerX, asteroidsComponent.centerY);
		asteroids = new ArrayList<Asteroid>(20);
		
		int n = 10 + random.nextInt(6); // get between 10-16
		for (int i = 0; i < n; i++) {
			int x = random.nextInt(asteroidsComponent.width);
			int y = random.nextInt(asteroidsComponent.height);
			float r = 15 + random.nextInt(20); // get between 15-35
			int verts = 12;
			float radiusVariance = 0.2f * r;
			addAsteroid(asteroids, x, y, r, verts, radiusVariance);
		}
	}
	
	public void tick() {
		// update bullets
		for (Bullet b : bullets) {
			if (b.alive) {
				b.updatePos();
			}
		}
				
		// update asteroids
		for(Asteroid a : asteroids) {
			for (Bullet b : bullets) {
				if (Util.isPointInsideCircle(b.x, b.y, a.x, a.y, a.boundingRadius)) {
					b.alive = false;
					a.alive = false;
				}
			}
			
			a.update();
			
			// wrap around screen
			a.x = Util.wrap(a.x, asteroidsComponent.width);
			a.y = Util.wrap(a.y, asteroidsComponent.height);
		}
		
		// update player
		playerShip.update();
		playerShip.x = Util.wrap(playerShip.x, asteroidsComponent.width);
		playerShip.y = Util.wrap(playerShip.y, asteroidsComponent.height);
		
		// asteroid collisions
		collidingAsteroidPairs = new ArrayList<>();
		
		for(Asteroid asteroid : asteroids) {
			for (Asteroid target : asteroids) {
				// don't test against itself
				if (asteroid.asteroidId == target.asteroidId) {
					continue;
				}
				
				// check collision
				if (Util.doCirclesOverlap(asteroid.x, asteroid.y, asteroid.boundingRadius, target.x, target.y, target.boundingRadius)) {
					// collision has occurred
					collidingAsteroidPairs.add(new Asteroid[] {asteroid, target});
					
					// distance between centers
					double dist = Util.distance(asteroid.x, asteroid.y, target.x, target.y);
					double halfOverlap = 0.5 * (dist - asteroid.boundingRadius - target.boundingRadius);
					
					// normalized vector between centers
					double normalizedDx = (asteroid.x - target.x) / dist;
					double normalizedDy = (asteroid.y - target.y) / dist;
					
					// displace current asteroid
					asteroid.x -= halfOverlap * normalizedDx;
					asteroid.y -= halfOverlap * normalizedDy;
					
					// displace target asteroid
					target.x += halfOverlap * normalizedDx;
					target.y += halfOverlap * normalizedDy;
				}
			}
		}
		
		// now for dynamic asteroids
		for (Asteroid[] p : collidingAsteroidPairs) {
			Asteroid a1 = p[0];
			Asteroid a2 = p[1];
			
			// distance between asteroids
			float dist = (float) Util.distance(a1.x, a1.y, a2.x, a2.y);
			
			// normal vector
			float nx = (a1.x - a2.x) / dist;
			float ny = (a1.y - a2.y) / dist;
			
			// tangental vector
			float tx = -ny;
			float ty = nx;
			
			// dot product tangent
			float dpTan1 = a1.xVel * tx + a1.yVel * ty;
			float dpTan2 = a2.xVel * tx + a2.yVel * ty;
			
			// dot product normal
			float dpNorm1 = a1.xVel * nx + a1.yVel * ny;
			float dpNorm2 = a2.xVel * nx + a2.yVel * ny;
			
			// conversion of momentum in 1D
			float m1 = (dpNorm1 * (a1.mass - a2.mass) + 2.0f * a2.mass * dpNorm2) / (a1.mass + a2.mass);
			float m2 = (dpNorm2 * (a2.mass - a1.mass) + 2.0f * a1.mass * dpNorm1) / (a1.mass + a2.mass);
			
			a1.xVel = tx * dpTan1 + nx * m1;
			a1.yVel = ty * dpTan1 + ny * m1;
			a2.xVel = tx * dpTan2 + nx * m2;
			a2.yVel = ty * dpTan2 + ny * m2;
		}
		
		ArrayList<Asteroid> toAdd = new ArrayList<>();
		for (Asteroid a : asteroids) {
			if (!a.alive) {


				// choose how much to split
				int numSplit = 2 + random.nextInt(2); // between 2-4
				for (int i = 0; i < numSplit; i++) {
					float x = a.x + (5 + random.nextInt(10)); // between 5-15
					float y = a.y + (5 + random.nextInt(10)); // between 5-15
					addAsteroid(toAdd, x, y, a.baseRadius/2.0f, (int)(a.numVertices*.75f), a.radiusVariance/2.0f);
				}
				
			}
		}
		for (Asteroid a : toAdd) {
			asteroids.add(a);
		}
		
		// kill all things that need die
		bullets.removeIf(new Predicate<Bullet>() {
			public boolean test(Bullet t) {
				return !t.alive;
			}
		});
		
		// remove dead asteroids and split them up
		asteroids.removeIf(new Predicate<Asteroid>() {
			public boolean test(Asteroid a) {				
				return !a.alive;
			}
		});
	}
	
	public void addAsteroid(ArrayList<Asteroid> array, float x, float y, float radius, int numVertices, float radiusVariance) {
		Asteroid a = new Asteroid(x, y, radius, random, numVertices, radiusVariance);
		a.xVel = (float) random.nextGaussian() * 30;
		a.yVel = (float) random.nextGaussian() * 30;
		a.velAngle = (float) (random.nextGaussian() * .5);
		array.add(a);
//		System.out.println(a.toString());
	}
	
	public void removeAsteroid(int asteroidId) {
		asteroids.removeIf(new Predicate<Asteroid>() {
			public boolean test(Asteroid t) {
				return t.asteroidId == asteroidId;
			}
		});
	}
	
	public void shipShootBullet() {
		if (System.currentTimeMillis() - lastFireTime >= fireCooldown) {
			lastFireTime = System.currentTimeMillis();
			float playerSpeed = Util.distance(playerShip.xVel, playerShip.yVel, 0, 0); // get magnitude
			float playerNoseX = playerShip.getCurrentModelInts()[0][0];
			float playerNoseY = playerShip.getCurrentModelInts()[0][1];
			Bullet b = new Bullet(playerNoseX, playerNoseY, playerShip.angle, playerSpeed + 150);
			bullets.add(b);
		}
	}
	
	public void render(Graphics2D g) {
		VectorGraphics vg = new VectorGraphics(g, asteroidsComponent.width, asteroidsComponent.height);
		
		vg.getGraphics().setColor(Color.black);
		vg.getGraphics().fillRect(0, 0, asteroidsComponent.width, asteroidsComponent.height);
		
		for (Asteroid a : asteroids) {
			a.draw(vg);
		}
		
		playerShip.draw(vg);
		
		for (Bullet b : bullets) {
			b.draw(vg);
		}
		
		// debug draw
//		int i = -1;
//		for (Asteroid a : asteroids) {
//			a.drawLayer(g, i);
//		}
		
//		playerShip.drawLayer(g, i);
	}
}
