import time
from operator import add

from Framework import Model
from Framework.Camera import Camera
from Framework.GameObjects import GameObject
from Framework.GameObjects import UpdatableGameobject
from Framework.GameObjects.Bike import Bike
from Framework.GameObjects.HumanPlayer import HumanPlayer
from Framework.GameObjects.AIPlayer import AIPlayer
from Framework.GameObjects.Sphere import Sphere
from Framework.KeyboardHandler import KeyboardHandler
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo


class Scene(KeyboardHandler):
    def __init__(self):
        self.gameObjects = []

        self.bot = AIPlayer(position = [0, 500, 0])
        self.addGameObject(self.bot)

        self.human = HumanPlayer(position = [0, 500, 0], keyboardHandler = self)
        self.addGameObject(self.human)

        sphereObject = Sphere(position = [0, 0, 0], color=[0, 0, 0, 1])
        self.addGameObject(sphereObject)

        self.lastUpdate = time.time() * 1000
        self.camera = Camera([0,0,100],[0,0,0],[0,1,0])
        self.fps = 0
        self.fps_track = []
        self.fps_time = time.time()

        KeyboardHandler.__init__(self)

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def render(self):
        self.gameObjects.sort(key = lambda x : 1 if x.isTransparent() else 0)

        for gameObject in self.gameObjects:
            gameObject.render()

        self.camera.render()

    def renderUI(self, x, y):
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, x, 0, y)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDepthMask(False)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glPushMatrix()

        #render UI
        self.drawSpeedBar(x, y)
        self.drawEnergyBar(x, y)
        self.drawFps()

        glPopMatrix()
        glDepthMask(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

    def drawSpeedBar(self, x, y):
        startX = x - x * 0.01
        endY = y * 0.5

        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex3f(startX - 1, endY + 1, -0.02)
        glVertex3f(startX - 1, 0, -0.02)
        glVertex3f(x, 0, -0.02)
        glVertex3f(x, endY + 1, -0.02)
        glEnd()

        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex3f(startX, endY, -0.02)
        glVertex3f(startX, 0, -0.02)
        glVertex3f(x, 0, -0.02)
        glVertex3f(x, endY, -0.02)
        glEnd()

        endY = y * 0.5 * self.human.speed / self.human.maxSpeed

        glColor3f(0, 0, 1)
        glBegin(GL_QUADS)
        glVertex3f(startX, endY, -0.02)
        glVertex3f(startX, 0, -0.02)
        glVertex3f(x, 0, -0.02)
        glVertex3f(x, endY, -0.02)
        glEnd()


    def drawEnergyBar(self, x, y):
        startX = x - x * 0.02 - 1
        endX = x - x * 0.01 - 1
        endY = y * 0.5

        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex3f(startX - 1, endY + 1, -0.02)
        glVertex3f(startX - 1, 0, -0.02)
        glVertex3f(endX + 1, 0, -0.02)
        glVertex3f(endX + 1, endY + 1, -0.02)
        glEnd()

        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex3f(startX, endY, -0.02)
        glVertex3f(startX, 0, -0.02)
        glVertex3f(endX, 0, -0.02)
        glVertex3f(endX, endY, -0.02)
        glEnd()
        endY = y * 0.5 * self.human.cloakEnergy / self.human.maxCloakEnergy

        glColor3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(startX, endY, -0.02)
        glVertex3f(startX, 0, -0.02)
        glVertex3f(endX, 0, -0.02)
        glVertex3f(endX, endY, -0.02)
        glEnd()


    def drawFps(self):
        glPushMatrix()
        glScalef(0.1, 0.1, 0.1)
        glTranslatef(10,30,0)
        glColor3f(0, 1, 0)

        for c in "{0:.2f}".format(self.fps):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(c))

        glPopMatrix()


    def update(self):
        #update the scene
        delta = time.time() * 1000 - self.lastUpdate
        for gameObject in self.gameObjects:
            if hasattr(gameObject, 'update'):
                if gameObject is self.human:
                    gameObject.update(delta, self.camera, self.bot)
                elif gameObject is self.bot:
                    gameObject.update(delta, self.camera, self.human)
                else:
                    gameObject.update(delta, self.camera)



        self.lastUpdate += delta
        self.fps_track.append(delta)
        self.fps_track = self.fps_track[-10:] #track last 10 framerate

        if time.time() - self.fps_time > 0.2:
            self.fps = 1000 / (reduce(lambda x, y: x + y, self.fps_track) / len(self.fps_track))
            self.fps_time = time.time()
        self.down_keys = set()

        return