from OpenGL.GL import *

from PIL import Image

from LibGL.Helpers import *

# =========================================
# Scene rendering

class SceneRenderer:

    bounds = 0.0
    texture = 0
    a1 = 0.0
    a2 = 0.0

    def __init__(self, width, height):

        self.bounds = 1.
        self.texture = LoadTexture("wp.bmp")

        glClearColor(0.2,0.2,0.2,1)
        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, (2.0, 2.0, 2.0))

        self.ResizeViewport(width, height)


    def ResizeViewport(self, width, height):

        aspect = 1.*width / height

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        b = self.bounds
        if width >= height :
            glOrtho(-b * aspect, b * aspect, -b, b, -b*1.5, b*1.5)
        else:
            glOrtho(-b, b, -b / aspect, b / aspect, -b*1.5, b*1.5)




    def RotateView(self, a1, a2):
        self.a1 += a1
        self.a2 += a2


    def Render(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor(0.,1.,0.,1.)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotated(self.a1, 0., 1., 0.)
        glRotated(self.a2, 1., 0., 0.)

        #SolidCube(-0.5, -0.5, -0.5, 0.5, 0.5, 0.5, self.texture)

        glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1,0,0,1))
        SolidCube(0, -0.1, -0.1, 0.9, 0.1, 0.1, 0)

        glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0,1,0,1))
        SolidCube(-0.1, 0, -0.1, 0.1, 0.9, 0.1, 0)

        glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0,0,1,1))
        SolidCube(-0.1, -0.1, 0, 0.1, 0.1, 0.9, 0)

        SolidCube(0.3, 0.3, 0.3, 0.7, 0.7, 0.7, self.texture)

        glFlush()

