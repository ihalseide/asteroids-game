package izak.asteroids;

public class Vector2F {

	public float x, y;
	
	public Vector2F() {
		this(0, 0);
	}
	
	public Vector2F(float[] arr) {
		this(arr[0], arr[1]);
	}
	
	public Vector2F(float v) {
		this(v, v);
	}
	
	public Vector2F(float x, float y) {
		this.x = x;
		this.y = y;
	}
	
	public float[] toArray() {
		return new float[] {x, y};
	}
}
