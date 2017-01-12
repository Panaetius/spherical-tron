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
        self.previousPosition = position
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
        self.active = True
        self.cloaked = False
        self.maxCloakEnergy = 1000
        self.cloakEnergy = self.maxCloakEnergy
        self.cloakEnergyDrain = 1000 # energy per second
        self.energyGain = 0.1


    def update(self, deltaTime, camera):
        self.previousPosition = self.position
        self.direction = (self.direction / np.linalg.norm(self.direction)).tolist()
        rot_mat = self.rotation_matrix(self.direction, self.speed * deltaTime / 1000)
        self.position = (np.dot(rot_mat, self.position)).tolist()

        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)

        self.collisionSphereCenter = self.position + (5.8 - self.collisionSphereRadius) * dir

        if self.checkCollisionWithTrail(self.trail):
            sys.exit(0) #you lost

        if self.speed > 0 and not self.cloaked:
            self.addTrail()

        if self.cloaked:
            self.cloakEnergy -= deltaTime * self.cloakEnergyDrain/1000
            if self.cloakEnergy < 0:
                self.cloaked = False
        elif self.cloakEnergy < self.maxCloakEnergy:
            self.cloakEnergy = max(self.maxCloakEnergy, self.cloakEnergy + deltaTime * self.energyGain)

        return

    def render(self):
        color = self.color[:]

        if self.cloaked:
            color[3] = 0.5
            glDepthMask(False)

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

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
        glDepthMask(True)

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
        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)
        currentTime = time.time() * 1000
        #trail should extend below sphere and behind the center of the bike for intersection
        self.trail.append([np.array(self.position) - 5*unit_pos - 0.2 * dir, self.position + self.trailHeight * unit_pos - 0.2 * dir, currentTime])
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
                    return True

            if distance > self.collisionSphereRadius:
                continue

            #check if the sphere is actually within the rectangle
            intersect = self.collisionSphereCenter - distance * normal
            t = intersect - point
            l1 = np.linalg.norm(v1)
            l2 = np.linalg.norm(v2)
            d1 = np.dot(t, v1/l1)
            d2 = np.dot(t, v2/l2)

            if d1 > -distance and d1 < l1 + distance and d2 > -distance and d2 < l2 + distance:
                return True



        return False