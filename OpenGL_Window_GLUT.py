from OpenGL.GLUT import *
import sys

from SceneRenderer import *

global render

def specialkeys(key, x, y):
    global render

    if key == GLUT_KEY_UP:
        render.RotateView(0., 5.)
    if key == GLUT_KEY_DOWN:
        render.RotateView(0., -5.)
    if key == GLUT_KEY_LEFT:
        render.RotateView(5., 0.)
    if key == GLUT_KEY_RIGHT:
        render.RotateView(-5., 0.)

    glutPostRedisplay()


def draw():
    global render
    render.Render()
    glutSwapBuffers()

def main():
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(50, 50)
    glutInit(sys.argv)
    glutCreateWindow(b"OpenGL GLUT Window")
    glutDisplayFunc(draw)
    glutSpecialFunc(specialkeys)

    global render
    render = SceneRenderer(300, 300)

    glutMainLoop()


main()