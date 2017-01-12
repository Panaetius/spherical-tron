from OpenGL.GL import *

from math import *

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
        self.acceleration = 2.0
        self.maxSpeed = 10


    def update(self, deltaTime, camera):
        if self.keyboardHandler.keyDown(Keys.LEFT):
            self.direction = np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyDown(Keys.RIGHT):
            self.direction = -np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyPressed(Keys.UP):
            self.speed = min(self.maxSpeed, self.speed + self.acceleration * deltaTime/1000)
        elif self.keyboardHandler.keyPressed(Keys.DOWN):
            self.speed = max(0.0, self.speed - self.acceleration * deltaTime/1000)

        self.direction = (self.direction / np.linalg.norm(self.direction)).tolist()
        rot_mat = self.rotation_matrix(self.direction, self.speed * deltaTime / 1000)
        self.position = (np.dot(rot_mat, self.position)).tolist()

        # forward = np.cross(self.position, self.direction)
        # forward = forward / np.linalg.norm(forward)
        #
        # up = np.array(self.position) / np.linalg.norm(self.position)
        #
        # left = np.cross(up, forward)
        #
        # mat = np.array([[-left[0], -left[1], -left[2], 0],
        #                 [-up[0], -up[1], -up[2], 0],
        #                 [-forward[0], -forward[1], -forward[2], 0],
        #                 [self.position[0], self.position[1], self.position[2], 1]])
        #
        # camera.viewmatrix = mat

        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)
        unit_pos = np.array(self.position)/np.linalg.norm(self.position)
        camera.position =  np.array(self.position) - 15 * dir + 5*unit_pos
        camera.lookat = np.array(self.position)
        camera.up = unit_pos#-np.array(self.bikeObject.position) / np.linalg.norm(self.bikeObject.position)

        return

    def render(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        #glTranslate(self.position[0], self.position[1], self.position[2])

        #orientation
        # obj_forward = [0,0,1]
        # obj_up = [0,-1,0]

        # up_angle = np.degrees(np.arccos(np.dot(obj_up, np.array(self.position))/(np.linalg.norm(self.position))))
        # up_rot = np.cross(obj_up, np.array(self.position))
        #
        # forward = np.cross(self.position, self.direction)
        # rot_mat = self.rotation_matrix(up_rot, -up_angle)
        # forward = np.dot(rot_mat, forward)
        #
        # forward_angle = np.degrees(np.arccos(np.dot(obj_forward, forward) / (np.linalg.norm(forward) * np.linalg.norm(obj_forward))))
        # forward_rot = np.cross(obj_forward, forward)
        #
        # glRotate(forward_angle, forward_rot[0], forward_rot[1], forward_rot[2])
        # glRotate(up_angle, up_rot[0], up_rot[1], up_rot[2])

        forward = np.cross(self.position, self.direction)
        forward = forward/np.linalg.norm(forward)

        up = np.array(self.position)/np.linalg.norm(self.position)

        left = np.cross(up, forward)

        mat = np.array([[left[0], left[1], left[2], 0],
                        [up[0], up[1], up[2], 0],
                        [forward[0], forward[1], forward[2], 0],
                        [self.position[0], self.position[1], self.position[2], 1]])
        glPushMatrix()
        glMultMatrixd(mat)
        glCallList(self.model.gl_list)
        glPopMatrix()

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