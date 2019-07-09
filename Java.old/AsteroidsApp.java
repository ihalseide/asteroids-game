package izak.asteroids;

import java.applet.Applet;
import java.awt.BorderLayout;

public class AsteroidsApp extends Applet {

	private static final long serialVersionUID = 1L;
	private AsteroidsComponent asteroids;

	public void init()
    {
		asteroids = new AsteroidsComponent(getWidth()/2, getHeight()/2);
        this.setLayout(new BorderLayout());
        add(asteroids, BorderLayout.CENTER);
    }
    
    public void start()
    {
    	asteroids.unpause();
    }
    
    public void stop()
    {
    	asteroids.pause();
    }

    public void destroy()
    {
    	asteroids.stop();
    }

}
