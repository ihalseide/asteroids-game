package izak.asteroids;

import java.awt.Color;

public class Bullet extends SpaceObject {
	
	public Bullet(float x, float y, float angle, float speed) {
		this.x = x;
		this.y = y;
		this.angle = angle;
		this.xVel = (float) (Math.cos(angle) * speed);
		this.yVel = (float) (Math.sin(angle) * speed);
		this.velAngle = 0;
	}
	
	public void draw(VectorGraphics vg) {
		vg.getGraphics().setColor(Color.red);
		vg.drawPoint((int) x, (int) y);
	}
	
	public Vector2F[] getCurrentModel() {
		return new Vector2F[] {new Vector2F(x, y)};
	}
}
