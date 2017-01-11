from Framework import GameObject
from Framework import Model
from operator import add

class Scene(object):
    def __init__(self):
        self.gameObjects = []
        bikeModel = Model.Model('Assets/Models/bike.obj')
        self.bikeObject = GameObject.GameObject(bikeModel, position = [1,0,0], xRotation=10, yRotation=30, zRotation=60)
        self.addGameObject(self.bikeObject)

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def render(self):
        for gameObject in self.gameObjects:
            gameObject.render()

    def update(self):
        #update the scene

        return

    def keyboard(self, ch, x, y):
        return

    def keyboard_special(self, ch, x, y):
        if ch == 100:
            #Left
            self.bikeObject.position = map(add, self.bikeObject.position, [-0.1, 0, 0])
        elif ch == 102:
            #right
            self.bikeObject.position = map(add, self.bikeObject.position, [0.1, 0, 0])
        elif ch == 101:
            #up
            self.bikeObject.position = map(add, self.bikeObject.position, [0, 0.1, 0])
        elif ch == 103:
            #down
            self.bikeObject.position = map(add, self.bikeObject.position, [0, -0.1, 0])

        return