import math
import random
from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Circle
from pyglet.graphics import Batch
from pyglet import clock


class Planet:
    def __init__(self, x, y, vx, vy, radius, color, batch):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.circle = Circle(x, y, radius, color=color, batch=batch)


class GravityChaos(Window):
    def __init__(self):
        super().__init__(1400, 900, vsync=True)
        self.batch = Batch()
        self.cx = self.width // 2
        self.cy = self.height // 2
        
        # Base scale (depends on screen size)
        self.world_scale = min(self.width, self.height)

        # Sun
        self.sun = Circle(
            self.cx,
            self.cy,
            int(0.03 * self.world_scale),
            color=(255, 255, 100),
            batch=self.batch
            )

        #self.gravity = 0.12 * self.world_scale
        
        self.gravity = 200 * self.world_scale
        # Create planets
        self.planets = []

         # Stable-ish orbit

        self.planets.append(Planet(self.cx + (0.2 * self.world_scale), self.cy, 0, 0.02 * self.world_scale,
        0.01 * self.world_scale, (100, 200, 255), self.batch))
        
        # Slightly unstable (shaky)
        self.planets.append(
            Planet(
                self.cx + 0.25 * self.world_scale,
                self.cy,
                0,
                0.018 * self.world_scale,
                0.012 * self.world_scale,
                (255, 100, 200),
                self.batch
            )
        )

        # Very unstable (chaotic)
        self.planets.append(
            Planet(
                self.cx + 0.35 * self.world_scale,
                self.cy,
                0,
                0.015 * self.world_scale,
                0.012 * self.world_scale,
                (200, 255, 100),
                self.batch
            )
        )


        # Random chaos planets
        for _ in range(3):
            x = self.cx + random.uniform(0.15, 0.4) * self.world_scale
            y = self.cy
            vx = random.uniform(-0.01, 0.01) * self.world_scale
            vy = random.uniform(0.015, 0.025) * self.world_scale   

            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255),
            )

            self.planets.append(
                Planet(x, y, vx, vy, 0.01 * self.world_scale, color, self.batch)
            )



    def update(self, dt):
        for p in self.planets:
            dx = self.cx - p.x
            dy = self.cy - p.y

            dist = math.sqrt(dx * dx + dy * dy)
            dist = max(0.1 * self.world_scale, dist)

            # normalize
            dx /= dist
            dy /= dist

            # gravity
            force = self.gravity / (dist * dist + (0.1 * self.world_scale)**2)

            ax = dx * force
            ay = dy * force

            # update velocity
            p.vx += ax * dt
            p.vy += ay * dt

            # clamp speed (INSIDE loop!)
            speed = math.sqrt(p.vx * p.vx + p.vy * p.vy)
            max_speed = 0.08 * self.world_scale

            if speed > max_speed:
                p.vx = (p.vx / speed) * max_speed
                p.vy = (p.vy / speed) * max_speed

            # Move planet
            p.x += p.vx * dt
            p.y += p.vy * dt

            p.circle.x = p.x
            p.circle.y = p.y

    def on_draw(self):
        self.clear()
        self.batch.draw()


game = GravityChaos()
clock.schedule_interval(game.update, 1/60)

run()