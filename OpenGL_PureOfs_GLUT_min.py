from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image
from PIL import ImageOps

import sys

width, height = 300, 300

def init():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glColor(0.0, 1.0, 0.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glViewport(0, 0, width, height)

def render():

    glClear(GL_COLOR_BUFFER_BIT)

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


def draw():
    render()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(300, 300)
    glutCreateWindow(b"OpenGL Offscreen")
    glutHideWindow()

    init()
    render()

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
    image.save('glut.png', 'PNG')

    #glutDisplayFunc(draw)
    #glutMainLoop()

main()