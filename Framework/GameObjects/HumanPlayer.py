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


class HumanPlayer(Bike):

   def update(self, deltaTime, camera):
        if self.keyboardHandler.keyDown(Keys.LEFT):
            self.direction = -np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyDown(Keys.RIGHT):
            self.direction = np.cross(self.direction, self.position)
        elif self.keyboardHandler.keyPressed(Keys.UP):
            self.speed = min(self.maxSpeed, self.speed + self.acceleration * deltaTime/1000)
        elif self.keyboardHandler.keyPressed(Keys.DOWN):
            self.speed = max(0.0, self.speed - self.acceleration * deltaTime/1000)
        elif self.keyboardHandler.keyDown(Keys.SPACE):
            self.cloaked = True
            self.trail = []

        self.direction = (self.direction / np.linalg.norm(self.direction)).tolist()
        rot_mat = self.rotation_matrix(self.direction, self.speed * deltaTime / 1000)
        self.position = (np.dot(rot_mat, self.position)).tolist()

        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)

        self.collisionSphereCenter = self.position + (5.8 - self.collisionSphereRadius) * dir

        if self.speed > 0 and not self.cloaked:
            self.addTrail()

        if self.checkCollisionWithTrail(self.trail):
            sys.exit(0) #you lost

        if self.cloaked:
            self.cloakEnergy -= deltaTime * self.cloakEnergyDrain/1000
            if self.cloakEnergy < 0:
                self.cloaked = False
        elif self.cloakEnergy < self.maxCloakEnergy:
            self.cloakEnergy = max(self.maxCloakEnergy, self.cloakEnergy + deltaTime * self.energyGain)


        #set camera to follow camera
        unit_pos = np.array(self.position)/np.linalg.norm(self.position)
        camera.position =  np.array(self.position) - 15 * dir + 8*unit_pos + 0.1 * np.array(self.direction)
        camera.lookat = np.array(self.position)
        camera.up = unit_pos

        return