package izak.asteroids;

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferStrategy;
import java.awt.image.VolatileImage;

import javax.swing.JFrame;

public class AsteroidsComponent extends Canvas implements Runnable, KeyListener, MouseListener, MouseMotionListener {

	private static final long serialVersionUID = 1L;
	
	public static final int TICKS_PER_SECOND = 30;
	public static final int MAX_TICKS_PER_FRAME = 10;
	public static final double MS_PER_TICK = 1.0 / TICKS_PER_SECOND;
    
    public static void main(String[] args) {    	
        final AsteroidsComponent asteroids = new AsteroidsComponent(512, 320);

        JFrame frame = new JFrame("Asteroids");
        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
            	asteroids.stop();
                System.exit(0);
            }
        });
        frame.setResizable(false);
        frame.add(asteroids);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        
        asteroids.start();
    }

    private boolean running;
    private VolatileImage image;
    private Thread thread;
    private int tickCount;
    private int frames;
    private boolean paused;
    
    boolean[] keysPressed;
    
    int width, height;
    final int centerX, centerY;
    
    SpaceZone spaceZone;

	public AsteroidsComponent(int width, int height) {
		this.width = width;
		this.height = height;
		centerX = width / 2;
		centerY = height / 2;
		setSize(width * 2, height * 2); // scaled up pixels
		setPreferredSize(new Dimension(width * 2, height * 2));
		setMaximumSize(new Dimension(width * 2, height * 2));
		setMinimumSize(new Dimension(width * 2, height * 2));
		addKeyListener(this);
		addMouseListener(this);
		addMouseMotionListener(this);
		keysPressed = new boolean[256];
	}
	
	public void init() {
		
		spaceZone = new SpaceZone(this);
		
	}
	
	public void start() {
		thread = new Thread(this, "Game Thread");
		thread.start();
	}
	
	public void pause() {
		paused = true;
	}
	
	public void unpause() {
		if (thread == null) {
			start();
		}
		paused = false;
	}
	
	public void stop() {
		running = false;
		try {
			if (thread != null) {
				thread.join();
			}
		}
		catch (InterruptedException e) {
			// pass
		}
	}
	
	public void run() {
		init();
		
        float lastTime = (System.nanoTime() / 1000000) / 1000.0f;
        running = true;
       
        while (running) {
            synchronized (this) {
                float now = (System.nanoTime() / 1000000) / 1000.0f;
                int frameTicks = 0;
                while (now - lastTime > MS_PER_TICK) {
                    if (!paused && frameTicks++ < MAX_TICKS_PER_FRAME) tick();

                    lastTime += MS_PER_TICK;
                }

                if (!paused) {
                    render((now - lastTime) / MS_PER_TICK);
                }
            }

            try {
                Thread.sleep(paused ? 200 : 4);
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
	}
	
	public void tick() {
		tickCount++;
		spaceZone.tick();
	}
	
	public void render(double alpha) {
		frames++;
        BufferStrategy bs = getBufferStrategy();
        if (bs == null)
        {
            createBufferStrategy(2);
            bs = getBufferStrategy();
        }

        if (image == null)
        {
            image = createVolatileImage(width, height);
        }

        if (bs != null)
        {
            Graphics2D g = image.createGraphics();
            renderGame(g, alpha);
            g.dispose();

            Graphics gg = bs.getDrawGraphics();
            gg.drawImage(image, 0, 0, width * 2, height * 2, 0, 0, width, height, null);
            gg.dispose();
            bs.show();
        }
	}

	private void renderGame(Graphics2D g, double alpha) {
		spaceZone.render(g);
		
		// HUD
		VectorGraphics vg = new VectorGraphics(g, width, height);
		int seconds = tickCount / TICKS_PER_SECOND;
		
		//
		g.setColor(Color.white);
		vg.drawLine(5, 5, 10, 5);
	}
	
	public void keyPressed(KeyEvent e) {
		int k = e.getKeyCode();
		keysPressed[k] = true;
		
		if (k == KeyEvent.VK_LEFT || k == KeyEvent.VK_A) {
			spaceZone.playerShip.turning = -1;
		}
		else if (k == KeyEvent.VK_RIGHT || k == KeyEvent.VK_D) {
			spaceZone.playerShip.turning = 1;
		}
		else if (k == KeyEvent.VK_UP || k == KeyEvent.VK_W) {
			spaceZone.playerShip.isThrusting = true;
		}
		else if (k == KeyEvent.VK_SPACE) {
			spaceZone.shipShootBullet();
		}
		else if (k == KeyEvent.VK_ESCAPE) {
			if (paused) {
				unpause();
			}
			else {
				pause();
			}
		}
	}
	
	public void keyReleased(KeyEvent e) {
		int k = e.getKeyCode();
		keysPressed[k] = false;
		
		if (k == KeyEvent.VK_LEFT || k == KeyEvent.VK_A || k == KeyEvent.VK_RIGHT || k == KeyEvent.VK_D) {
			spaceZone.playerShip.turning = 0;
		}
		else if (k == KeyEvent.VK_UP || k == KeyEvent.VK_W) {
			spaceZone.playerShip.isThrusting = false;
		}
	}
	
	public void keyTyped(KeyEvent e) { }

	public void mouseDragged(MouseEvent e) { }
	
	public void mouseMoved(MouseEvent e) { }
	
	public void mouseClicked(MouseEvent e) { }
	
	public void mouseEntered(MouseEvent e) { }
	
	public void mouseExited(MouseEvent e) { }
	
	public void mousePressed(MouseEvent e) { }
	
	public void mouseReleased(MouseEvent e) { }
}
