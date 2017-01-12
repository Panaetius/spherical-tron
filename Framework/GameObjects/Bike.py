from OpenGL.GL import *

from math import *
import time
import sys

from OpenGL.arrays import vbo

from Framework import Model
from Framework.GameObjects.GameObject import GameObject
from Framework.GameObjects.KeyboardObject import KeyboardObject
from Framework.GameObjects.UpdatableGameobject import UpdatableGameobject
from Framework.KeyboardHandler import Keys
import numpy as np
from OpenGL.GLU import *


class Bike(GameObject, KeyboardObject, UpdatableGameobject):
    def __init__(self, position=[50.0, 0.0, 0.0], xRotation=0.0, yRotation=0.0, zRotation=0.0, color = [1.0,1.0,1.0,1.], keyboardHandler = None):
        bikeModel = Model.Model('Assets/Models/bike.obj')
        GameObject.__init__(self, bikeModel, position=position, xRotation=xRotation, yRotation=yRotation, zRotation=zRotation, color=color)
        KeyboardObject.__init__(self, keyboardHandler)
        self.direction = [0, 0, 1]
        self.speed = 0.0
        self.acceleration = 1.0
        self.maxSpeed = 5
        self.trail = []
        self.trailLength = 3
        self.trailHeight = 5
        self.trailColor = [0, 0, 1, 0.75]
        self.collisionSphereRadius = 1.2
        self.collisionSphereCenter = np.array([0,0,0])


    def update(self, deltaTime, camera):
        if self.keyboardHandler.keyDown(Keys.LEFT):
            self.direction = -np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyDown(Keys.RIGHT):
            self.direction = np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyPressed(Keys.UP):
            self.speed = min(self.maxSpeed, self.speed + self.acceleration * deltaTime/1000)
        elif self.keyboardHandler.keyPressed(Keys.DOWN):
            self.speed = max(0.0, self.speed - self.acceleration * deltaTime/1000)

        self.direction = (self.direction / np.linalg.norm(self.direction)).tolist()
        rot_mat = self.rotation_matrix(self.direction, self.speed * deltaTime / 1000)
        self.position = (np.dot(rot_mat, self.position)).tolist()

        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)

        self.collisionSphereCenter = self.position + (5.8 - self.collisionSphereRadius) * dir

        if self.speed > 0:
            self.addTrail()

        if self.checkCollisionWithTrail(self.trail):
            sys.exit(0) #you lost

        #set camera to follow camera
        unit_pos = np.array(self.position)/np.linalg.norm(self.position)
        camera.position =  np.array(self.position) - 15 * dir + 8*unit_pos + 0.1 * np.array(self.direction)
        camera.lookat = np.array(self.position)
        camera.up = unit_pos

        return

    def render(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)

        #calculate world matrix for rotation&position
        forward = np.cross(self.position, self.direction)
        forward = forward/np.linalg.norm(forward)

        up = np.array(self.position)/np.linalg.norm(self.position)

        left = np.cross(up, forward)

        mat = np.array([[left[0], left[1], left[2], 0],
                        [up[0], up[1], up[2], 0],
                        [forward[0], forward[1], forward[2], 0],
                        [self.position[0], self.position[1], self.position[2], 1]])
        glPushMatrix()
        #set world matrix
        glMultMatrixd(mat)

        #render
        glCallList(self.model.gl_list)
        glPopMatrix()
        self.renderTrail()

    def rotation_matrix(self, axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / sqrt(np.dot(axis, axis))
        a = cos(theta / 2.0)
        b, c, d = -axis * sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def addTrail(self):
        unit_pos = np.array(self.position)/np.linalg.norm(self.position)
        currentTime = time.time() * 1000
        self.trail.append([np.array(self.position), self.position + self.trailHeight * unit_pos, currentTime])
        self.trail = [t for t in self.trail if currentTime - t[2] < self.trailLength * 1000]

    def renderTrail(self):
        if len(self.trail) < 2:
            return

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.trailColor)

        glBegin(GL_QUAD_STRIP)

        for i in range(0, len(self.trail), 1):
            current = self.trail[i]
            glVertex3f(current[1][0], current[1][1], current[1][2])
            glVertex3f(current[0][0], current[0][1], current[0][2])

        glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(0, len(self.trail), 1):
            current = self.trail[i]
            glVertex3f(current[0][0], current[0][1], current[0][2])
            glVertex3f(current[1][0], current[1][1], current[1][2])

        glEnd()

    def checkCollisionWithTrail(self, trail):
        for i in range(0, len(self.trail) - 1, 1):
            first = trail[i]
            second = trail[i + 1]
            point = first[0]
            v1 = first[1] - first[0]
            v2 = second[0] - first[0]
            normal = np.cross(v1, v2)
            normal = normal/np.linalg.norm(normal)
            distance = np.dot(self.collisionSphereCenter - point, normal)

            if distance > self.collisionSphereRadius:
                continue

            #check if the sphere is actually within the rectangle
            intersect = self.collisionSphereCenter - distance * normal
            t = intersect - point
            d1 = np.dot(t, v1)
            d2 = np.dot(t, v2)
            l1 = np.linalg.norm(v1)
            l2 = np.linalg.norm(v2)

            if d1 < -distance or d1 > l1 + distance or d2 < -distance or d2 > l2 + distance:
                continue

            return True

        return False