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

        v1 = np.cross(self.direction, self.position)
        v1 = v1 / np.linalg.norm(v1)

        v2 = np.cross(enemy.position, self.position)
        v2 = v2 / np.linalg.norm(v2)
        dot = np.dot(v1,v2)
            

        if dot < -0.6:
            self.direction = -np.cross(self.direction, self.position)
        elif dot > 0.6:
            self.direction = np.cross(self.direction, self.position)

        Bike.update(self, deltaTime, camera, enemy)

        return