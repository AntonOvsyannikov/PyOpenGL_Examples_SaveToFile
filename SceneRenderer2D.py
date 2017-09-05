from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# =========================================
# Scene rendering

class SceneRenderer:

    a1 = 0.0
    a2 = 0.0

    def __init__(self, width, height):

        glClearColor(0.5, 0.5, 0.5, 1.0)
        glColor(0.0, 1.0, 0.0)
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
        glViewport(0, 0, width, height)

        self.ResizeViewport(width, height)

    def ResizeViewport(self, width, height):
        glViewport(0, 0, width, height)

    def RotateView(self, a1, a2):
        pass

    def Render(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotated(self.a1, 0., 1., 0.)
        glRotated(self.a2, 1., 0., 0.)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw xy axis with arrows
        glBegin(GL_LINES)

        # x
        glVertex2d(-1, 0)
        glVertex2d(1, 0)
        glVertex2d(1, 0)
        glVertex2d(0.95, 0.05)
        glVertex2d(1, 0)
        glVertex2d(0.95, -0.05)

        # y
        glVertex2d(0, -1)
        glVertex2d(0, 1)
        glVertex2d(0, 1)
        glVertex2d(0.05, 0.95)
        glVertex2d(0, 1)
        glVertex2d(-0.05, 0.95)

        glEnd()

        glFlush()

