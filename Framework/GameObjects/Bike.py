from operator import add

from Framework import Model
from Framework.GameObjects.GameObject import GameObject
from Framework.GameObjects.KeyboardObject import KeyboardObject
from Framework.GameObjects.UpdatableGameobject import UpdatableGameobject
from Framework.KeyboardHandler import Keys


class Bike(GameObject, KeyboardObject, UpdatableGameobject):
    def __init__(self, position=[0.0, 0.0, 0.0], xRotation=0.0, yRotation=0.0, zRotation=0.0, color = [1.0,1.0,1.0,1.], keyboardHandler = None):
        bikeModel = Model.Model('Assets/Models/bike.obj')
        GameObject.__init__(self, bikeModel, position, xRotation, yRotation, zRotation, color)
        KeyboardObject.__init__(self, keyboardHandler)


    def update(self):
        if self.keyboardHandler.keyPressed(Keys.LEFT):
            self.position = map(add, self.position, [-0.1, 0, 0])
        elif self.keyboardHandler.keyPressed(Keys.RIGHT):
            self.position = map(add, self.position, [0.1, 0, 0])
        elif self.keyboardHandler.keyPressed(Keys.UP):
            self.position = map(add, self.position, [0, 0.1, 0])
        elif self.keyboardHandler.keyPressed(Keys.DOWN):
            self.position = map(add, self.position, [0, -0.1, 0])