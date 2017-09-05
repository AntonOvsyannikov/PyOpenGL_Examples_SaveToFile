'''
Offscreen rendering using WGL default buffers with hidden window
Standalone code - not using LibGL from this repository
'''

from win32api import *
from win32con import *
from win32gui import *

from OpenGL.WGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image
from PIL import ImageOps

import uuid

# =========================================
# I left here only necessary constants, it's easy to search for the rest

PFD_TYPE_RGBA =         0
PFD_MAIN_PLANE =        0
PFD_DOUBLEBUFFER =      0x00000001
PFD_DRAW_TO_WINDOW =    0x00000004
PFD_SUPPORT_OPENGL =    0x00000020

# =========================================
# OpenGL context creation helpers

def mywglCreateContext(hWnd):
    pfd = PIXELFORMATDESCRIPTOR()

    # note - we don't using double buffering
    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL
    pfd.iPixelType = PFD_TYPE_RGBA
    pfd.cColorBits = 32
    pfd.cDepthBits = 24
    pfd.iLayerType = PFD_MAIN_PLANE

    hdc = GetDC(hWnd)

    pixelformat = ChoosePixelFormat(hdc, pfd)
    SetPixelFormat(hdc, pixelformat, pfd)

    oglrc = wglCreateContext(hdc)
    wglMakeCurrent(hdc, oglrc)

    # check is context created succesfully
    # print "OpenGL version:", glGetString(GL_VERSION)


def mywglDeleteContext():
    hrc = wglGetCurrentContext()
    wglMakeCurrent(0, 0)
    if hrc: wglDeleteContext(hrc)


# =========================================
# Scene rendering

def renderInit(width, height):

    glClearColor(0.5, 0.5, 0.5, 1.0)
    glColor(0.0, 1.0, 0.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glViewport(0, 0, width, height)


def render():

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

# =========================================
# Windows stuff and main steps

def main():

    # Create window first with Win32 API

    hInstance = GetModuleHandle(None)

    wndClass = WNDCLASS()

    wndClass.lpfnWndProc = DefWindowProc
    wndClass.hInstance = hInstance
    wndClass.hbrBackground = GetStockObject(WHITE_BRUSH)
    wndClass.hCursor = LoadCursor(0, IDC_ARROW)
    wndClass.lpszClassName = str(uuid.uuid4())
    wndClass.style = CS_OWNDC

    wndClassAtom = RegisterClass(wndClass)

    # we care about window size, because we use default buffers, associated with the window
    width, height = 300, 300
    hWnd = CreateWindow(wndClassAtom, '', WS_POPUP, 0, 0, width, height, 0, 0, hInstance, None)

    # Ok, window created, now we can create OpenGL context

    mywglCreateContext(hWnd)

    # Init our renderer
    renderInit(width, height)

    # Now everything is ready for job to be done!
    # Render something and save it to file

    render()

    glReadBuffer(GL_FRONT)

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason

    image.save("wgl.png", "PNG")

    # Shutdown everything
    mywglDeleteContext()

main()