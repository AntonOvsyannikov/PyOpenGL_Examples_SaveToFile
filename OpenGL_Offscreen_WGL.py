'''
Offscreen rendering using WGL default buffers with hidden window
'''

from PIL import Image
from PIL import ImageOps

from LibGL.Win32 import *
from LibGL.Context import *

from Renderers.Renderer3D import *

# =========================================
# Windows stuff and main steps

def main():

    # we care about window size, because we use default buffers, associated with the window
    # also don't forget WS_POPUP style, otherwise render area will differ from window size

    width, height = 300, 300
    hWnd = CreateWindowA( size = (width, height), style = WS_POPUP )

    # actually we create WS_POPUP window with no border and caption, so this call is not necessary
    x,y,width, height = GetClientRect(hWnd)

    # Ok, window created, now we can create OpenGL context

    CreateContext(hWnd, doubleBuffer=False) # or you can use default doublebuffer context, but don't forget to read GL_BACK buffer instead of GL_FRONT

    # Init our renderer
    render = SceneRenderer(width, height)

    # Now everything is ready for job to be done!
    # Render something and save it to file

    render.Render()

    glReadBuffer(GL_FRONT)

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason

    image.save("wgl1.png", "PNG")

    # Shutdown everything
    DeleteContext()

main()