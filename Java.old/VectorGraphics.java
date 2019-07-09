package izak.asteroids;

import java.awt.Graphics2D;

public class VectorGraphics {

	private Graphics2D g;
	private final int screenWidth, screenHeight;
	
	public VectorGraphics(Graphics2D g, int screenWidth, int screenHeight) {
		this.g = g;
		this.screenWidth = screenWidth;
		this.screenHeight = screenHeight;
	}
	
	public Graphics2D getGraphics() {
		return g;
	}
	
	public void drawPoint(int x, int y) {
		g.fillRect(x, y, 1, 1);
	}
	
	public void drawWrapPoint(int x, int y) {
		int sx = Math.round(Util.wrap(x, screenWidth));
		int sy = Math.round(Util.wrap(y, screenHeight));
		drawPoint(sx, sy);
	}
	
	public void drawLine(int x1, int y1, int x2, int y2) {
		// Bresenham's line algorithm
		int dx = Math.abs(x2 - x1);
		int sx = (x1 < x2) ? 1 : -1;
		int dy = -Math.abs(y2 - y1);
		int sy = (y1 < y2) ? 1 : -1;
		int err = dx + dy; /* error value e_xy */
		while (true) {
			drawPoint(x1, y1);
			if (x1 == x2 && y1 == y2)
				break;
			int e2 = 2 * err;
			if (e2 >= dy) {
				err += dy; /* e_xy+e_x > 0 */
				x1 += sx;
			}
			if (e2 <= dx) {/* e_xy+e_y < 0 */
				err += dx;
				y1 += sy;
			}
		}
				
		/* OLD Bresenham's line algorithm
		int x = x1;
		int y = y1;
		int dx = x2 - x1;
		int dy = y2 - y1;
		
		// If slope < 1
		if (dx > dy) {
			int p = 2*dx-dy;
			while (x < x2) {
				drawPoint(x, y);
				x++;
				if (p < 0) {
					p = p + 2*dy;
				}
				else {
					p = p + (2*dy) - (2*dx);
					y++;
				}
			}
		}
		else { // Slope >= 1
			int p = 2*dy-dx;
			while (y < y2) {
				drawPoint(x, y);
				y++;
				if (p < 0) {
					p = p + 2*dx;
				}
				else {
					p = p + (2*dx) - (2*dy);
					x++;
				}
			}
		}
		*/
		
		/*// DDA line drawing
		int dx = x2 - x1;
		int dy = y2 - y1;
		int numSteps = Math.max(dx, dy);
		float xInc = (float)(dx) / (float)(numSteps);
		float yInc = (float)(dy) / (float)(numSteps);
		for (int i = 0; i < numSteps; i++) {
			int x = x1 + Math.round(i * xInc);
			int y = y1 + Math.round(i * yInc);
			drawPoint(x, y);
		}
		*/
	}
	
	public void drawWrapLine(int x1, int y1, int x2, int y2) {
		// Bresenham's line algorithm
		int dx = Math.abs(x2 - x1);
		int sx = (x1 < x2) ? 1 : -1;
		int dy = -Math.abs(y2 - y1);
		int sy = (y1 < y2) ? 1 : -1;
		int err = dx + dy; /* error value e_xy */
		while (true) {
			drawWrapPoint(x1, y1);
			if (x1 == x2 && y1 == y2)
				break;
			int e2 = 2 * err;
			if (e2 >= dy) {
				err += dy; /* e_xy+e_x > 0 */
				x1 += sx;
			}
			if (e2 <= dx) {/* e_xy+e_y < 0 */
				err += dx;
				y1 += sy;
			}
		}
	}
	
	public void drawLines(int[][] points, boolean closed) {
		int x, y;
		int startX = points[0][0], startY = points[0][1];
		int prevX = startX, prevY = startY;
		for (int i = 1; i < points.length; i++) {
			x = points[i][0];
			y = points[i][1];
			drawLine(prevX, prevY, x, y);
			prevX = x;
			prevY = y;
		}
		if (closed) {
			drawLine(prevX, prevY, startX, startY);
		}
	}
	
	public void drawWrapLines(int[][] points, boolean closed) {
		int x, y;
		int startX = points[0][0], startY = points[0][1];
		int prevX = startX, prevY = startY;
		for (int i = 1; i < points.length; i++) {
			x = points[i][0];
			y = points[i][1];
			drawWrapLine(prevX, prevY, x, y);
			prevX = x;
			prevY = y;
		}
		if (closed) {
			drawWrapLine(prevX, prevY, startX, startY);
		}
	}
	
	public void drawEllipse(float cx, float cy, float rx, float ry) { 
		float dx, dy, d1, d2, x, y;
		x = 0;
		y = ry;

		// Initial decision parameter of region 1
		d1 = (ry * ry) - (rx * rx * ry) + (0.25f * rx * rx);
		dx = 2 * ry * ry * x;
		dy = 2 * rx * rx * y;

		// For region 1
		while (dx < dy) {
			// Checking and updating value of
			// decision parameter based on algorithm
			drawPoint((int)(cx + x), (int)(cy + y));
			drawPoint((int)(cx + x), (int)(cy - y));
			drawPoint((int)(cx - x), (int)(cy + y));
			drawPoint((int)(cx - x), (int)(cy - y));
			if (d1 < 0) {
				x++;
				dx = dx + (2 * ry * ry);
				d1 = d1 + dx + (ry * ry);
			} 
			else {
				x++;
				y--;
				dx = dx + (2 * ry * ry);
				dy = dy - (2 * rx * rx);
				d1 = d1 + dx - dy + (ry * ry);
			}
		}

		// Decision parameter of region 2
		d2 = ((ry * ry) * ((x + 0.5f) * (x + 0.5f))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry);

		// Plotting points of region 2
		while (y >= 0) {
			// Checking and updating parameter
			// value based on algorithm
			drawPoint((int)(cx + x), (int)(cy + y));
			drawPoint((int)(cx + x), (int)(cy - y));
			drawPoint((int)(cx - x), (int)(cy + y));
			drawPoint((int)(cx - x), (int)(cy - y));
			if (d2 > 0) {
				y--;
				dy = dy - (2 * rx * rx);
				d2 = d2 + (rx * rx) - dy;
			} else {
				y--;
				x++;
				dx = dx + (2 * ry * ry);
				dy = dy - (2 * rx * rx);
				d2 = d2 + dx - dy + (rx * rx);
			}
		}
	}
	
	public void drawWrapEllipse(float cx, float cy, float rx, float ry) { 
		float dx, dy, d1, d2, x, y;
		x = 0;
		y = ry;

		// Initial decision parameter of region 1
		d1 = (ry * ry) - (rx * rx * ry) + (0.25f * rx * rx);
		dx = 2 * ry * ry * x;
		dy = 2 * rx * rx * y;

		// For region 1
		while (dx < dy) {
			// Checking and updating value of
			// decision parameter based on algorithm
			drawWrapPoint((int)(cx + x), (int)(cy + y));
			drawWrapPoint((int)(cx + x), (int)(cy - y));
			drawWrapPoint((int)(cx - x), (int)(cy + y));
			drawWrapPoint((int)(cx - x), (int)(cy - y));
			if (d1 < 0) {
				x++;
				dx = dx + (2 * ry * ry);
				d1 = d1 + dx + (ry * ry);
			} 
			else {
				x++;
				y--;
				dx = dx + (2 * ry * ry);
				dy = dy - (2 * rx * rx);
				d1 = d1 + dx - dy + (ry * ry);
			}
		}

		// Decision parameter of region 2
		d2 = ((ry * ry) * ((x + 0.5f) * (x + 0.5f))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry);

		// Plotting points of region 2
		while (y >= 0) {
			// Checking and updating parameter
			// value based on algorithm
			drawWrapPoint((int)(cx + x), (int)(cy + y));
			drawWrapPoint((int)(cx + x), (int)(cy - y));
			drawWrapPoint((int)(cx - x), (int)(cy + y));
			drawWrapPoint((int)(cx - x), (int)(cy - y));
			if (d2 > 0) {
				y--;
				dy = dy - (2 * rx * rx);
				d2 = d2 + (rx * rx) - dy;
			} else {
				y--;
				x++;
				dx = dx + (2 * ry * ry);
				dy = dy - (2 * rx * rx);
				d2 = d2 + dx - dy + (rx * rx);
			}
		}
	}
}
