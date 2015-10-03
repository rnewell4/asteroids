import pygame as PG
import random as R
import math
from ship import *
from rocks import *
from constants import *

class Missile (PhysicsObject):
    """Bullets shot by ship in the same direction in which the ship is facing.
    When it makes contact with asteroids, it makes them explode."""
    def __init__(self, Ship):
        self.t = 0
        self.center=Ship.getCorners()[0]
        ref = array([MSPEED, 0])
        self.vel = Ship.vel + rotate(Ship.angle, ref, (0,0))
        self.corners = [self.center]

    def draw(self, surface):
        """draws missle"""
        PG.draw.circle(surface, [255, 255, 255], toInt(self.center), 1)

    def update(self, dt):
        """updates position of missle"""
        self.t += dt
        self.center += self.vel * dt
        self.corners = [self.center]


class Thrust (PhysicsObject):
    """Red articles emitted from the back of the ship that travel in the
    oppposite direction in which the ship was facing."""
    def __init__(self, Ship):
        self.t = 0
        ref = array([-SSIZE, 0])
        self.center = Ship.center + rotate(Ship.angle, ref, (0,0))
        ref = array([-.5*MSPEED, 0])
        angle = Ship.angle -math.pi/6 + R.random()
        self.vel = -Ship.vel + rotate(angle, ref, (0, 0))
        self.red = R.randint(200, 255)
        self.blue = R.randint(0, 120)
        self.green = R.randint(0, 150)
        self.corners = [self.center]

    def draw(self, surface):
        PG.draw.circle(surface, [self.red, self.blue, self.green],
                       toInt(self.center), 0)

    def update(self, dt):
        """updates position of fire"""
        self.t += dt
        self.center += self.vel*dt/2
        self.corners = [self.center]


class Debris(PhysicsObject):
    """Particles emitting radially away from a central position that was the
    location of a previously drawn ship or asteroid that only appears when the
    ship or asteroid get destroyed."""
    def __init__(self, obj, size):
        self.t = 0
        self.velocity = 20
        self.radius = size / 10
        self.center = obj.center  

    def draw(self, surface):
        self.angle = []
        for i in range(50):
            a = R.random() * math.pi * 2
            self.angle.append(a)
        ref1 = array([self.radius, 0])
        ref2 = array([self.radius - 2, 0])
        ref3 = array([self.radius - 3, 0])
        ref4 = array([self.radius - 4, 0])
        for angle in self.angle:
            p1 = rotate(angle, ref1, (0,0)) + self.center
            p2 = rotate(angle, ref2, (0,0)) + self.center
            p3 = rotate(angle, ref3, (0,0)) + self.center
            p4 = rotate(angle, ref4, (0,0)) + self.center

            PG.draw.circle(surface, (255, 0, 0), toInt(p1), 0)
            PG.draw.circle(surface, (255, 0, 0), toInt(p2), 0)
            PG.draw.circle(surface, (255, 0, 0), toInt(p3), 0)
            PG.draw.circle(surface, (255, 0, 0), toInt(p4), 0)

    def update(self, dt):
        """updates position of fire"""
        self.t += dt*5
        self.radius = self.radius + self.velocity*dt*10
