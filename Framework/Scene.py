from Framework import GameObject
from Framework import Model
from operator import add

class Scene(object):
    def __init__(self):
        self.gameObjects = []
        bikeModel = Model.Model('Assets/Models/bike.obj')
        self.addGameObject(GameObject.GameObject(bikeModel, position = [1,0,0], xRotation=10, yRotation=30, zRotation=60))

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def render(self):
        for gameObject in self.gameObjects:
            gameObject.render()

    def update(self):
        #update the scene
        for gameObject in self.gameObjects:
            gameObject.position = map(add,gameObject.position,[0.1, 0, 0])