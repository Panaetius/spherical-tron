from OpenGL.GL import *
from OpenGL.GLU import *

class Camera(object):
    def __init__(self, position, lookat, up):
        self.position = position
        self.lookat = lookat
        self.up = up

    def render(self):
        #glPushMatrix()
        # glMatrixMode(GL_PROJECTION)
        # gluPerspective(40., 1., 1., 300.)
        # glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glLoadIdentity()
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.lookat[0], self.lookat[1], self.lookat[2],
                  self.up[0], self.up[1], self.up[2])
        glPushMatrix()
        #glPopMatrix()