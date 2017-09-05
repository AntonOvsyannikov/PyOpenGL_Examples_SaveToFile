from OpenGL.WGL import *
from PFD import *
from win32gui import *

'''
Important! PyOpenGL 3.1.1 have a bug!

When you just import WGL, glReadPixels() starts to crash with

ctypes.ArgumentError: argument 7: : wrong type

Go to [package dir]\OpenGL\raw\WGL_types.py , find the following lines

HANDLE = POINTER(None)  # /home/mcfletch/pylive/OpenGL-ctypes/src/wgl.h:60
# TODO: figure out how to make the handle not appear as a void_p within the code...
HANDLE.final = True

replace by

HANDLE = UINT64 # for x64, UINT32 for x86
HANDLE.final = True

'''

# =========================================
# OpenGL context creation helpers

def CreateContext(hWnd, doubleBuffer = True, colorBits = 32, depthBits = 24, pixelType = PFD_TYPE_RGBA):
    pfd = PIXELFORMATDESCRIPTOR()

    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | (PFD_DOUBLEBUFFER if doubleBuffer else 0)
    pfd.iPixelType = pixelType
    pfd.cColorBits = colorBits
    pfd.cDepthBits = depthBits
    pfd.iLayerType = PFD_MAIN_PLANE

    hdc = GetDC(hWnd)

    pixelformat = ChoosePixelFormat(hdc, pfd)
    SetPixelFormat(hdc, pixelformat, pfd)

    oglrc = wglCreateContext(hdc)
    wglMakeCurrent(hdc, oglrc)

    # check is context created succesfully
    # print "OpenGL version:", glGetString(GL_VERSION)


def DeleteContext():
    hrc = wglGetCurrentContext()
    wglMakeCurrent(0, 0)
    if hrc: wglDeleteContext(hrc)