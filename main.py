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
    # initialize glut window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    width=1024
    height=768
    glutInitWindowSize(width, height)
    glutCreateWindow(name)

    # set shader and defaults
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_POLYGON_OFFSET_LINE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # add light
    lightZeroPosition = [10., 4., 10., 1.]
    lightZeroColor = [0.8, 1.0, 0.8, 1.0]  # green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.01)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
    glEnable(GL_LIGHT0)

    # set glut functions
    glutDisplayFunc(display)
    glutIdleFunc(gameloop)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboardUp)
    glutSpecialFunc(keyboard_special)
    glutSpecialUpFunc(keyboard_specialUp)

    # set camera projection, position and direction
    glMatrixMode(GL_PROJECTION)
    gluPerspective(75., width/height, 1., 300.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(10, 101, 0,
              0, 101, 0,
              0, 1, 0)

    # init scene
    scene = Scene.Scene()

    glutMainLoop()
    return


def display():
    global scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0, 0., 0., 1.]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

    scene.render()

    glPopMatrix()
    glutSwapBuffers()
    return


def gameloop():
    # main game loop, called repeatedly
    global scene
    scene.update()
    glutPostRedisplay()
    return


def keyboard(ch, x, y):
    global scene
    scene.keyboard(ch, x, y)
    glutPostRedisplay()
    return 0


def keyboardUp(ch, x, y):
    global scene
    scene.keyboardUp(ch, x, y)
    glutPostRedisplay()
    return 0


def keyboard_special(ch, x, y):
    global scene
    scene.keyboard_special(ch, x, y)
    glutPostRedisplay()
    return 0

def keyboard_specialUp(ch, x, y):
    global scene
    scene.keyboard_specialUp(ch, x, y)
    glutPostRedisplay()
    return 0


if __name__ == '__main__': main()
