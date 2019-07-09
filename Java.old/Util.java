package izak.asteroids;

public class Util {

	public static float wrap(final float i, final float limit) {
		// modulus dealing with negatives correctly
		if (i >= 0) {
			return i % limit;
		}
		else {
			return (limit + i) % limit;
		}
	}
	
	public static boolean isPointInsideCircle(float px, float py, float cx, float cy, float cRadius) {
		return distance(px, py, cx, cy) < cRadius;
	}
	
	public static float[] arrDoubleToFloat(final double[] arr) {
		float[] output = new float[arr.length];
		for (int i = 0; i < arr.length; i++) {
			output[i] = (float) arr[i];
		}
		return output;
	}
	
	public static int[] arrFloatToInt(final float[] arr) {
		int[] output = new int[arr.length];
		for (int i = 0; i < arr.length; i++) {
			output[i] = (int) arr[i];
		}
		return output;
	}

	public static float distanceSquared(float x1, float y1, float x2, float y2) {
		float dx = x1 - x2;
		float dy = y1 - y2;
		return dx*dx + dy*dy;
	}
	
	public static float distance(float x1, float y1, float x2, float y2) {
		return (float) Math.sqrt(distanceSquared(x1, y1, x2, y2));
	}
	
	public static boolean doCirclesOverlap(float x1, float y1, float r1, float x2, float y2, float r2) {
		return distance(x1, y1, x2, y2) <= r1 + r2;
	}
	
	public static Vector2F translatePoint(float x, float y, float dx, float dy) {
		float nx = x + dx;
		float ny = y + dy;
		return new Vector2F(nx, ny);
	}
	
	public static Vector2F scalePoint(float x, float y, float xScale, float yScale) {
		float nx = x * xScale;
		float ny = y * yScale;
		return new Vector2F(nx, ny);
	}
	
	public static Vector2F rotatePoint(float x, float y, float angle) {
		double cos = Math.cos(angle);
		double sin = Math.sin(angle);
		float nx = (float) (x*cos - y*sin);
		float ny = (float) (y*cos + x*sin);
		return new Vector2F(nx, ny);
	}
	
	public static Vector2F transformPoint(float x, float y, float dx, float dy, float angle, float xScale, float yScale) {
		Vector2F newPoint;
		newPoint = scalePoint(x, y, xScale, yScale);
		newPoint = rotatePoint(newPoint.x, newPoint.y, angle);
		newPoint = translatePoint(newPoint.x, newPoint.y, dx, dy);
		return newPoint;
	}
	
	public static Vector2F[] transformPoints(final Vector2F[] points, float dx, float dy, float angle, float xScale, float yScale) {
		Vector2F[] newPoints = new Vector2F[points.length];
		for (int i = 0; i < points.length; i++) {
			float x = points[i].x;
			float y = points[i].y;
			newPoints[i] = transformPoint(x, y, dx, dy, angle, xScale, yScale);
		}
		return newPoints;
	}
	
	public static float min(float[] arr) {
		float currentMin = arr[0];
		for(int i = 0; i < arr.length; i++) {
			if(arr[i] < currentMin) {
				currentMin = arr[i];
			}
		}
		return currentMin;
	}
	
	public static float max(float[] arr) {
		float currentMax = arr[0];
		for(int i = 0; i < arr.length; i++) {
			if(arr[i] > currentMax) {
				currentMax = arr[i];
			}
		}
		return currentMax;
	}
	
	public static float sum(float[] arr) {
		float total = 0;
		for (float v : arr) {
			total += v;
		}
		return total;
	}
	
	public static float avg(float[] arr) {
		return sum(arr) / arr.length;
	}

	public static float mapValue(float val, float minIn, float maxIn, float minOut, float maxOut) {
		return val;
	}
}
