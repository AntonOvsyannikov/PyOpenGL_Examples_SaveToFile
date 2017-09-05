'''
Offscreen rendering using manually created OpenGL Framebuffer Object
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
# OpenGL Framebuffer Objects helpers

def myglCreateBuffers(width, height):

    fbo = glGenFramebuffers(1)
    color_buf = glGenRenderbuffers(1)
    depth_buf = glGenRenderbuffers(1)

    # binds created FBO to context both for read and draw
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    # bind color render buffer
    glBindRenderbuffer(GL_RENDERBUFFER, color_buf)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, width, height)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_buf)

    # bind depth render buffer - no need for 2D, but necessary for real 3D rendering
    glBindRenderbuffer(GL_RENDERBUFFER, depth_buf)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buf)

    return fbo, color_buf, depth_buf, width, height

def myglDeleteBuffers(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteRenderbuffers(1, color_buf)
    glDeleteRenderbuffers(1, depth_buf)
    glDeleteFramebuffers(1, fbo)

def myglReadColorBuffer(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(GL_COLOR_ATTACHMENT0)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    return data, width, height

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

    # don't care about window size, couse we will create independent buffers
    hWnd = CreateWindow(wndClassAtom, '', WS_POPUP, 0, 0, 1, 1, 0, 0, hInstance, None)

    # Ok, window created, now we can create OpenGL context

    mywglCreateContext(hWnd)

    # In OpenGL context create Framebuffer Object (FBO) and attach Color and Depth render buffers to it

    width, height = 300, 300
    buffers = myglCreateBuffers(width, height)

    # Init our renderer
    renderInit(width, height)

    # Now everything is ready for job to be done!
    # Render something and save it to file

    render()

    data, width, height = myglReadColorBuffer(buffers)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason

    # it's easy to achive antialiasing effect by resizing rendered image
    # don't forget to increase initial rendered image resolution and line thikness for 2D
    #image = image.resize((width/2, height/2), Image.ANTIALIAS)

    image.save("fbo.png", "PNG")

    # Shutdown everything
    myglDeleteBuffers(buffers)
    mywglDeleteContext()

main()