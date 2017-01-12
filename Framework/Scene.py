import time

from Framework import Model
from Framework.GameObjects import GameObject
from Framework.GameObjects import UpdatableGameobject
from Framework.GameObjects.Bike import Bike
from Framework.KeyboardHandler import KeyboardHandler


class Scene(KeyboardHandler):
    def __init__(self):
        self.gameObjects = []

        self.bikeObject = Bike(position = [50.0, 0, 0], xRotation=10, yRotation=30, zRotation=60, keyboardHandler = self)
        self.addGameObject(self.bikeObject)

        sphereModel = Model.Model('Assets/Models/Sphere.obj')
        sphereObject = GameObject.GameObject(sphereModel, color=[0, 0.5, 0, 0.5])
        self.addGameObject(sphereObject)

        self.lastUpdate = time.time() * 1000

        KeyboardHandler.__init__(self)

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def render(self):
        for gameObject in self.gameObjects:
            gameObject.render()

    def update(self):
        #update the scene
        delta = time.time() * 1000 - self.lastUpdate
        for gameObject in self.gameObjects:
            if hasattr(gameObject, 'update'):
                gameObject.update(delta)

        self.lastUpdate = time.time() * 1000
        self.down_keys = set()

        return