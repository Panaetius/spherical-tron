from OpenGL.GL import *

class GameObject(object):
    def __init__(self, model, position=[0.0, 0.0, 0.0], xRotation=0.0, yRotation=0.0, zRotation=0.0, color = [1.0,1.0,1.0,1.]):
        self.model = model
        self.position = position
        self.xRotation = xRotation
        self.yRotation = yRotation
        self.zRotation = zRotation
        self.color = color

    def render(self):
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        glTranslate(self.position[0], self.position[1], self.position[2])
        glRotate(self.xRotation, 1, 0, 0)
        glRotate(self.yRotation, 0, 1, 0)
        glRotate(self.zRotation, 0, 0, 1)
        glCallList(self.model.gl_list)