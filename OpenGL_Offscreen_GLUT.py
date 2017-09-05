'''
Offscreen rendering using GLUT hidden window
'''

from OpenGL.GLUT import *

from PIL import Image
from PIL import ImageOps

import sys

from Renderers.Renderer3D import *

global render

def draw():
    render()
    glutSwapBuffers()

def main():

    width, height = 300, 300

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"OpenGL Offscreen")
    glutHideWindow()

    global render

    render = SceneRenderer(width, height)
    render.Render()

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
    image.save('glut1.png', 'PNG')

    #glutDisplayFunc(draw)
    #glutMainLoop()

main()