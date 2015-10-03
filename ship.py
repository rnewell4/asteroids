from physics import *
import pygame as PG
import random as R
"""Initial Conditions"""
# Screen size
SIZE = (1280, 720)
# Number of Asteroids created
ASTEROIDS = 2
# Size of asteroids
ASIZE = 50
# Speed of asteroids
SPEED = 20
# Speed of Bullets
MSPEED = 4200
# Size of Ship
SSIZE = 20
# Acceleration of Ship
ACCEL = 200
# Initial Score
SCORE = 0
# Initial Lives
LIVES = 3
# Initial Level
LEVEL = 1
# Maximum speed for ship
VMAX = 4000
# Maximum Frames per second
FPS = 60
# Life time of bullet
MAXT = .127
# Time dead
TDEAD = MAXT * 6
# minimum time between bullet shots
TIME_TO_PRESS = 210
# time ship is invincible
INV_TIME = .4

class Ship (PhysicsObject):
    """User guided object that moves and accelerates through space, shooting
    missiles and dying when hit by an asteroid."""
    def __init__(self):
        self.center = [SIZE[0] / 2, SIZE[1] / 2]
        super().__init__(array([SIZE[0] /2 , SIZE[1] /2]));
        self.angle = -math.pi / 2
        self.orientShip()
        self.time_Inv = INV_TIME

    def draw(self, surface):
        """Draws the ship"""
        self.red = 255 * R.random()
        self.green = 255 * R.random()
        self.blue = 255 * R.random()
        if self.is_Invincible():
            PG.draw.polygon(surface, (self.red, self.green, self.blue),
                            self.corners, 1)
        else:
            PG.draw.polygon(surface, (255, 255, 255), self.corners, 1)

    def orientShip(self):
        """Updates the corners of the ship"""
        self.corners = []
        ref = array([2*SSIZE, 0]) + self.center
        self.corners.append(rotate(self.angle, ref, self.center))
        ref = array([SSIZE, 0]) + self.center
        self.corners.append(rotate(self.angle + 125*math.pi/180,ref, self.center))
        self.corners.append(rotate(self.angle - 125*math.pi/180,ref, self.center))
    def set_invincible(self, t_inv=INV_TIME):
        """Makes ship invincible for a period of time"""
        self.time_Inv = t_inv

    def is_Invincible(self):
        """Checks invincibility."""
        return self.time_Inv > 0
    
    def update(self, delta):
        """Updates the ship after a time delta"""
        self.center += delta*self.vel
        self.orientShip()
        self.time_Inv -= delta

    def turn(self, theta):
        """Turns the ship"""
        self.angle += theta

    def accelerate(self, delta):
        """Increases the velocity based on the current angle up to a max of
        VMAX."""
        acelVec = array([delta*ACCEL, 0])
        acelVec = rotate(self.angle, acelVec, array([0, 0]))
        newVel = self.vel+acelVec
        if vector_magnitude(newVel) < VMAX:
            self.vel = newVel
