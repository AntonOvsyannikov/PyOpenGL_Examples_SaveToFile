from OpenGL.GL import *

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
# OpenGL Framebuffer Objects helpers

def CreateBuffers(width, height):

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

def DeleteBuffers(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteRenderbuffers(1, color_buf)
    glDeleteRenderbuffers(1, depth_buf)
    glDeleteFramebuffers(1, fbo)

def ReadColorBuffer(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(GL_COLOR_ATTACHMENT0)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    return data, width, height
