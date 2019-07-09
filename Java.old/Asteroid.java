package izak.asteroids;

import java.awt.Color;
import java.awt.Graphics2D;
import java.util.Random;

public class Asteroid extends SpaceObject {

	private static int lastAsteroidId = 0;
	private static final float DENSITY = 1;
	
	final Color darkBackground = new Color(15, 8, 8);
	
	final int asteroidId;
	final float mass;
	
	// radius and model information
	final float radiusVariance;
	final float baseRadius, averageRadius, minRadius, maxRadius, boundingRadius;
	final int numVertices;
	final Vector2F[] model;
	final float[] radii;
	Vector2F[] vertices;
	
	public Asteroid(float x, float y, float radius, Random random, int numVertices, float radiusVariance) {	
		// init stuffs
		this.x = x;
		this.y = y;
		this.angle = (float) (random.nextDouble() * 2 * Math.PI);
		this.baseRadius = radius;
		this.numVertices = numVertices;
		this.radiusVariance = radiusVariance;
		
		// init vertices
		model = new Vector2F[numVertices];
		vertices = new Vector2F[numVertices];
		radii = new float[numVertices];
		
		// populate model
		for (int i = 0; i < numVertices; i++) {
			// generate random radii
			float r = (float) (baseRadius + random.nextGaussian() * radiusVariance);
			radii[i] = r;
			// create vertices from trig around a circle
			double angle = 2 * Math.PI * ((double)i / (double)numVertices);
			float px = (float) (Math.cos(angle) * r);
			float py = (float) (Math.sin(angle) * r);
			model[i] = new Vector2F(px, py);
		}
		updateModel();
		
		averageRadius = Util.avg(radii);
		minRadius = Util.min(radii);
		maxRadius = Util.max(radii);
		
		// base collisions off of this radius
		boundingRadius = (maxRadius + averageRadius) / 2.0f;
		
		// calculate mass with consistent density
		mass = (float) (Math.PI * averageRadius*averageRadius * DENSITY);
		
		// deal with ids
		asteroidId = lastAsteroidId++;
	}
	
	private void updateModel() {
		// update model
		vertices = Util.transformPoints(model, x, y, angle, 1, 1);
	}
	
	public void update() {
		updatePos();
		updateModel();
	}
	
	public String toString() {
		return String.format("Asteroid:{x:%s, y:%s, r:%s, vx:%s, vy:%s, vr:%s, boundingRadius: %s, numVertices: %s", 
				x, y, angle, xVel, yVel, velAngle, boundingRadius, numVertices);
	}

	public Vector2F[] getCurrentModel() {
		return vertices;
	}
	
	public void draw(VectorGraphics vg) {
		Graphics2D g = vg.getGraphics();
//		// debug info
//		g.setColor(Color.white);
//		vg.drawEllipse(x, y, boundingRadius, boundingRadius);
//		vg.drawLine((int)(x - 3), (int)y, (int)(x+3), (int)y);
//		vg.drawLine((int)x, (int)(y - 3), (int)x, (int)(y+3));
		// draw red shape all around
		g.setColor(Color.yellow);
		vg.drawWrapLines(getCurrentModelInts(), true);
	}
}
