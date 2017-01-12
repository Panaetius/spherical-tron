import time
from operator import add

from Framework import Model
from Framework.Camera import Camera
from Framework.GameObjects import GameObject
from Framework.GameObjects import UpdatableGameobject
from Framework.GameObjects.Bike import Bike
from Framework.KeyboardHandler import KeyboardHandler
import numpy as np


class Scene(KeyboardHandler):
    def __init__(self):
        self.gameObjects = []

        self.bikeObject = Bike(position = [0, 500, 0], keyboardHandler = self)
        self.addGameObject(self.bikeObject)

        sphereModel = Model.Model('Assets/Models/Sphere.obj')
        sphereObject = GameObject.GameObject(sphereModel, position = [0, 0, 0], color=[0, 0.5, 0, 0.5], wireframe=True)
        self.addGameObject(sphereObject)

        self.lastUpdate = time.time() * 1000
        self.camera = Camera([0,0,100],[0,0,0],[0,1,0])

        KeyboardHandler.__init__(self)

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def render(self):
        # self.camera.render()

        for gameObject in self.gameObjects:
            gameObject.render()

        self.camera.render()

    def update(self):
        #update the scene
        delta = time.time() * 1000 - self.lastUpdate
        for gameObject in self.gameObjects:
            if hasattr(gameObject, 'update'):
                gameObject.update(delta, self.camera)



        self.lastUpdate = time.time() * 1000
        self.down_keys = set()

        return