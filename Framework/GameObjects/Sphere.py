from Framework import Model
from Framework.GameObjects.GameObject import GameObject
from OpenGL.GL import *


class Sphere(GameObject):
    def __init__(self, position, xRotation = 0, yRotation = 0, zRotation = 0, color = [0, 0, 0, 1]):
        sphereModel = Model.Model('Assets/Models/sphere.obj')
        GameObject.__init__(self, sphereModel, position=position, xRotation=xRotation, yRotation=yRotation,
                            zRotation=zRotation, color=color)


    def render(self):
        GameObject.render(self)

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1])
        glPushMatrix()

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glTranslate(self.position[0], self.position[1], self.position[2])
        glRotate(self.xRotation, 1, 0, 0)
        glRotate(self.yRotation, 0, 1, 0)
        glRotate(self.zRotation, 0, 0, 1)
        glCallList(self.model.gl_list)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL )

        glPopMatrix()