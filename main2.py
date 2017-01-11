import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLContext.arrays import *

from Framework import Model

name = 'spherical tron'

def main():
    #initialize glut window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1024,768)
    glutCreateWindow(name)

    #set shader and defaults
    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    #add light
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)

    #set display function
    glutDisplayFunc(display)

    #set camera projection, position and direction
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,30,
              0,0,0,
              0,1,0)
    glPushMatrix()
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,0.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    #glutSolidSphere(2,20,20)
    showBike()
    glPopMatrix()
    glutSwapBuffers()
    return

def showBike():
    #load and render the bike model
    bike = Model.Model('Assets/Models/bike.obj')

    glTranslate(1, 1., 0)
    glRotate(30, 1, 0, 0)
    glRotate(75, 0, 1, 0)
    glCallList(bike.gl_list)

    # try:
    #     bikeVBO.bind()
    #     glEnableClientState(GL_VERTEX_ARRAY)
    #
    #     glVertexPointer(2, GL_FLOAT, 0, bikeVBO)
    #     glColor(0, 1, 0, 1)
    #     glDrawArrays(GL_TRIANGLES , 0, bikeVBO.data.shape[0])
    #
    #     glDisableClientState(GL_VERTEX_ARRAY)
    # finally:
    #     bikeVBO.unbind()


if __name__ == '__main__': main()