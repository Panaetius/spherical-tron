from OpenGL.GL import *

from math import *
import time
import sys

from OpenGL.arrays import vbo

from Framework import Model
from Framework.GameObjects.GameObject import GameObject
from Framework.GameObjects.Bike import Bike
from Framework.GameObjects.KeyboardObject import KeyboardObject
from Framework.GameObjects.UpdatableGameobject import UpdatableGameobject
from Framework.KeyboardHandler import Keys
import numpy as np
from OpenGL.GLU import *


class AIPlayer(Bike):

   def __init__(self, position=[50.0, 0.0, 0.0], xRotation=0.0, yRotation=0.0, zRotation=0.0, color = [1.0,1.0,1.0,1]):
        Bike.__init__(self, position, xRotation, yRotation, zRotation, color)
        self.i = 0
        self.speed = 0.03

   def update(self, deltaTime, camera, enemy):
        trail = self.trail + enemy.trail
        trailFront = False
        collisionSphereRadius = 8

        # check if collision is near
        for i in range(0, len(trail) - 1, 1):
            first = trail[i]
            second = trail[i + 1]
            point = first[0]

            if np.linalg.norm(point - self.position) > collisionSphereRadius * 5:
                continue #don't do any collision checks for walls too far away

            v1 = first[1] - first[0]
            v2 = second[0] - first[0]
            normal = np.cross(v1, v2)
            normal = normal/np.linalg.norm(normal)
            distance = abs(np.dot(self.collisionSphereCenter - point, normal))

            if distance > 10:
                continue #too far away

            # check if we move through plane between frames
            pos = np.array(self.position)
            prev_pos = np.array(self.previousPosition)

            #raise pos up a bit since it's a the bottom of the model, so curvature means a direct line would go below the plane
            pos = pos + 0.5 * pos/np.linalg.norm(pos)
            prev_pos = prev_pos + 0.5 * prev_pos / np.linalg.norm(prev_pos)
            movement_ray = pos - prev_pos
            mov_len = np.linalg.norm(movement_ray)
            movement_ray = movement_ray / mov_len
            den = np.dot(normal, movement_ray)
            if abs(den) < 1e-6:
                continue  # parallel

            p0 = point - np.array(prev_pos)
            t = np.dot(p0, normal) / den
            if t > 1e-11 and t < mov_len:
                intersect = prev_pos + t * movement_ray
                i = intersect - point
                l1 = np.linalg.norm(v1)
                l2 = np.linalg.norm(v2)
                d1 = np.dot(i, v1/l1)
                d2 = np.dot(i, v2/l2)
                if d1 > 0 and d1 < l1  and d2 > 0 and d2 < l2:
                    trailFront = True
                    break

            if distance > collisionSphereRadius:
                continue

            #check if the sphere is actually within the rectangle
            intersect = self.collisionSphereCenter - distance * normal
            t = intersect - point
            l1 = np.linalg.norm(v1)
            l2 = np.linalg.norm(v2)
            d1 = np.dot(t, v1/l1)
            d2 = np.dot(t, v2/l2)

            if d1 > -distance and d1 < l1 + distance and d2 > -distance and d2 < l2 + distance:
                trailFront = True
                break
                

        rand = np.random.rand()

        if trailFront:
            self.direction = -np.cross(self.direction, self.position)
        #elif rand > 0.98:
        #    self.direction = np.cross(self.direction, self.position)

        Bike.update(self, deltaTime, camera, enemy)

        return