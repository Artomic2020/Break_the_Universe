import pyglet
import random
import math
from pyglet import shapes

WIDTH, HEIGHT = 1280, 720


class Particle:
    def __init__(self, x, y, vx, vy, life, batch):
        self.vx = vx
        self.vy = vy
        self.life = life
        self.radius = random.uniform(7.0, 13.0)
        self.circle = shapes.Circle(x, y, radius=self.radius, batch=batch)
        self.circle.color = (0, 20, 140)

    def update(self, dt):
        self.circle.x += self.vx * dt
        self.circle.y += self.vy * dt
        self.life -= dt

    def dead(self):
        return (
            self.life <= 0 or
            self.circle.x < -10 or self.circle.x > WIDTH + 10 or
            self.circle.y < -10 or self.circle.y > HEIGHT + 10
        )

    def delete(self):
        self.circle.delete()


class MyWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Particle Balls")

        self.batch = pyglet.graphics.Batch()
        self.particles = []

        self.emit_rate = 10              # particles per second
        self.time_since_emit = 1.0

        pyglet.clock.schedule_interval(self.on_update, 1/60)

    def emit_one(self):
        # Spawn at center with random velocity
        x = WIDTH / 2
        y = HEIGHT / 2
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 200)

        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed   # FIXED: use sin(angle) instead of constant speed
        vz = math.sin(angle) * speed
        
        life = random.uniform(1.5, 3.0)

        p = Particle(x, y, vx, vy, life, self.batch)
        self.particles.append(p)

    def on_update(self, dt):
        # Emitter timing (beginner-friendly)
        self.time_since_emit += dt
        time_per_particle = 1.0 / self.emit_rate

        while self.time_since_emit >= time_per_particle:
            self.emit_one()
            self.time_since_emit -= time_per_particle

        # Update particles
        for p in self.particles:
            p.update(dt)

        # Remove dead particles
        alive = []
        for p in self.particles:
            if p.dead():
                p.delete()
            else:
                alive.append(p)
        self.particles = alive

    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == "__main__":
    win = MyWindow()
    pyglet.app.run()
