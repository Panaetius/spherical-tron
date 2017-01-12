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


class HumanPlayer(Bike,KeyboardObject):
    def __init__(self, position=[50.0, 0.0, 0.0], xRotation=0.0, yRotation=0.0, zRotation=0.0, color=[1.0, 1.0, 1.0, 1.], keyboardHandler=None):
        KeyboardObject.__init__(self, keyboardHandler)
        Bike.__init__(self, position, xRotation, yRotation, zRotation, color)
        self.cloakAlpha = 0.4


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
            if not self.cloaked:
                self.cloaked = True
                self.trail = []
            else:
                self.cloaked = False

        Bike.update(self, deltaTime, camera)

        #set camera to follow camera
        dir = np.cross(self.direction, self.position)
        dir = dir / np.linalg.norm(dir)
        unit_pos = np.array(self.position)/np.linalg.norm(self.position)
        camera.position =  np.array(self.position) - 15 * dir + 8 * unit_pos + 0.1 * np.array(self.direction)
        camera.lookat = np.array(self.position)
        camera.up = unit_pos

        return
