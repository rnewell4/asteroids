import math
import sys
from numpy import *

def vectors_parallel(vec1, vec2):
    if not(len(vec1) == len(vec2)):
        raise ValueError
    mag = vector_magnitude(vec1)*vector_magnitude(vec2)
    return abs(dot(vec1, vec2)) == mag

def angle_between(vec1, vec2):
    return math.acos(dot(unitVec(vec1), unitVec(vec2)))

def vector_magnitude(vec):
    return dot(vec, vec)**(1/2)

def line_orthonormal(start, end):
    return orthonormal(start-end)

def unitVec(vec):
    length = vector_magnitude(vec)
    return vec/length

def orthonormal(vec):
    unit = unitVec(vec)
    return array((unit[1], -unit[0]))

def toInt(seq):
    try:
        #test if seq is a sequence
        seq[0]
        intseq = []
        for item in seq:
            intseq.append(toInt(item))
        return array(intseq)
    except:
        #if it isn't a sequence just type cast to int
        return int(seq)

def rotate(theta, coords, center):
    rot = array(((math.cos(theta), -math.sin(theta)),
                 (math.sin(theta), math.cos(theta))))
    rotated = dot(rot, (coords-center))
    return rotated + center

def projection(axis, corners):
    unit = unitVec(axis)
    newCorners = []
    for corner in corners:
        newCorners.append(dot(corner, unit))
    return newCorners

def get_axis_list(obj1):
    axis = []
    if len(obj1.getCorners())>1:
        for i in range(len(obj1.getCorners())):
            axis.append(obj1.getCorners()[i] - obj1.getCorners()[i-1])
    return axis

def collides(obj1, obj2):
    axis = get_axis_list(obj1)+get_axis_list(obj2)
    for a in axis:
        proj1 = projection(a, obj1.getCorners())
        proj2 = projection(a, obj2.getCorners())
        #Checks if projections overlap
        if not(max(proj1)<=max(proj2) and max(proj1)>=min(proj2)) and\
           not(min(proj1)<=max(proj2) and min(proj1)>=min(proj2)) and\
           not(max(proj2)<=max(proj1) and max(proj2)>=min(proj1)) and\
           not(min(proj2)<=max(proj1) and min(proj2)>=min(proj1)):
            return False
    return True

class PhysicsObject:
    def __init__(self, center,):
        self.center = center
        self.corners = []
        self.vel = array([0, 0])
        self.angle = 0

    def update(self, delta): 
        self.center += self.vel*delta

    def getCorners(self):
        return toInt(self.corners)

    def getVelocity(self):
        return toInt(self.vel)

        


