package izak.asteroids;

import java.awt.Color;
import java.awt.Graphics2D;

public class Ship extends SpaceObject {
	
	float scale = 15;
	float turnSpeed = 5.5f;
	float thrustAcceleration = 300f;
	float turnResistance = .45f;
	
	int turning; // -1, 0, or 1
	
	boolean isThrusting;
	boolean isFiring;
	
	final Vector2F[] model;
	Vector2F[] vertices;
	
	public Ship(int x, int y) {
		this.x = x;
		this.y = y;
		this.angle = 0;
		isThrusting = false;
		isFiring = false;
		turning = 0;
		
		float[][] tempModel = new float[][]{{1.0f, 0}, {-.4f, .5f}, {-.15f, 0}, {-.4f, -.5f}};
		model = new Vector2F[tempModel.length];
		for (int i = 0; i < model.length; i++) {
			model[i] = new Vector2F(tempModel[i][0], tempModel[i][1]);
		}
		
		vertices = new Vector2F[model.length];
		updateModel();
	}
	
	private void updateModel() {
		// update model
		vertices = Util.transformPoints(model, x, y, angle, scale, scale);
	}
	
	public void update() {		
		if(isThrusting) {
			// vector math
			xVel += (float)(Math.cos(angle) * thrustAcceleration / AsteroidsComponent.TICKS_PER_SECOND);
			yVel += (float)(Math.sin(angle) * thrustAcceleration / AsteroidsComponent.TICKS_PER_SECOND);
		}
		
		if (turning == 1) {
			velAngle = turnSpeed;
		}
		else if (turning == -1) {
			velAngle = - turnSpeed;
		}
		else {
			//pass
			velAngle *= 1.0 - turnResistance;
		}
		
		// add velocities
		updatePos();
		updateModel();
	}

	public Vector2F[] getCurrentModel() {
		return vertices;
	}
	
	public void draw(VectorGraphics vg) {		
		vg.getGraphics().setColor(Color.black);
		vg.getGraphics().setColor(Color.blue);
		vg.drawWrapLines(getCurrentModelInts(), true);
	}
}
