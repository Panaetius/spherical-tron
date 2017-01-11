import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLContext.arrays import *

from Framework import *
from Framework import Scene

name = 'spherical tron'

scene = ''

def main():
    global scene
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

    #set glut functions
    glutDisplayFunc(display)
    glutIdleFunc(gameloop)

    #set camera projection, position and direction
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,30,
              0,0,0,
              0,1,0)
    glPushMatrix()

    #init scene
    scene = Scene.Scene()

    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,0.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)

    scene.render()

    glPopMatrix()
    glutSwapBuffers()
    return

def gameloop():
    #main game loop, called repeatedly
    global scene
    scene.update()
    glutPostRedisplay()
    return

if __name__ == '__main__': main()