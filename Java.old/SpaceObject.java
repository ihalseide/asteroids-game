package izak.asteroids;

public abstract class SpaceObject {

	public float x, y, angle;
	public float xVel, yVel, velAngle;
	
	public boolean alive = true;
	
	public abstract Vector2F[] getCurrentModel();
	
	public void updatePos() {
		x += xVel / AsteroidsComponent.TICKS_PER_SECOND;
		y += yVel / AsteroidsComponent.TICKS_PER_SECOND;
		angle += velAngle / AsteroidsComponent.TICKS_PER_SECOND;
	}
	
	public void draw(VectorGraphics vg) {
		// pass
	}
	
	public int[][] getCurrentModelInts() {
		Vector2F[] model = getCurrentModel(); 
		int[][] modelInts = new int[model.length][2];
		for (int i = 0; i < model.length; i++) {
			modelInts[i][0] = Math.round(model[i].x);
			modelInts[i][1] = Math.round(model[i].y);
		}
		return modelInts;
	}
}
