import pygame as PG
import random as R
import math
import os
from ship import *
from constants import *
class Asteroid (PhysicsObject):
    """Randomly placed linearly-moving square object generated as the targets
    of the game. Explode when hit by missle and reduced in size until it
    disappears."""
    def __init__(self, order=3, start=[]):
        self.order = order
        self.size = self.order / 3 * ASIZE
        if start == []:
            width, height = SIZE
            start = [int(R.random()*width) + self.size/2,
                     int(R.random()*height) + self.size/2]
        theta = int(180 * R.random())
        ref = array([SPEED, 0])
        self.center = array([start[0], start[1]])
        self.vel=rotate(theta, ref, (0,0))
        self.createCorners()

    def draw(self, surface):
        """Draws asteroid"""
        if self.onScreen():
            PG.draw.polygon(surface, (255, 255, 255), self.corners, 1)

    def createCorners(self):
        """Creates corners of square asteroid"""
        length = self.size/2
        self.tlcor = self.center-array([length, length])
        self.trcor = self.center+array([length, -length])
        self.blcor = self.center+array([-length, length])
        self.brcor = self.center+array([length, length])
        self.corners = array([self.tlcor, self.trcor, self.brcor, self.blcor])

    def update(self, delta):
        """Moves the asteroid"""
        self.center += self.vel*delta
        self.createCorners()

    def onScreen(self):
        """Checks if the asteroid is onscreen"""
        ans = False
        for point in self.corners:
            if point[0] > 0 and point[0] < SIZE[0] and point[1] > 0 \
               and point[1] < SIZE[1]:
                ans = True
        return ans
