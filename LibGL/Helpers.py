from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

# =========================================
# Helpers

def SolidCube(x1, y1, z1, x2, y2, z2, texture):

    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_POLYGON)  # front face
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)  # back face
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y1, z1)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z1)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # left face
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x1, y2, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # right face
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(0, 1)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(0, 0)
    glVertex3f(x2, y1, z1)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y2, z1)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)  # top face
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y2, z1)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # bottom face
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x2, y1, z1)
    glEnd()

def LoadTexture(fileName):

    image = Image.open(fileName)
    width = image.size[0]
    height = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)  # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image)

    return texture

