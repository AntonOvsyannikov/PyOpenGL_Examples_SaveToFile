'''
Offscreen rendering using manually created OpenGL Framebuffer Object
'''

from PIL import Image
from PIL import ImageOps

from LibGL.Win32 import *
from LibGL.Context import *
from LibGL.Buffers import *

from Renderers.Renderer3D import *

# =========================================
# Windows stuff and main steps

def main():

    # Create window first with Win32 API
    # don't care about window size, cause we will create independent buffers

    hWnd = CreateWindowA(style = WS_POPUP)

    # Ok, window created, now we can create OpenGL context

    CreateContext(hWnd)

    # In OpenGL context create Framebuffer Object (FBO) and attach Color and Depth render buffers to it

    width, height = 300, 300
    buffers = CreateBuffers(width, height)

    # Init our renderer
    render = SceneRenderer(width, height)

    # Now everything is ready for job to be done!
    # Render something and save it to file

    render.Render()

    data, width, height = ReadColorBuffer(buffers)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason

    image.save("fbo1.png", "PNG")

    # Shutdown everything
    DeleteBuffers(buffers)
    DeleteContext()

main()