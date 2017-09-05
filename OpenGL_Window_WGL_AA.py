'''
Render using default WGL buffers in the second hidden window
Then resize rendered image with anti-aliasing and display it in the window
Use mouse to rotate the view
'''

from PIL import Image
from PIL import ImageWin
from PIL import ImageOps

from LibGL.Win32 import *
from LibGL.Context import *

from win32gui import *

from Renderers.Renderer3D import *

# =========================================
global render

global mouse_pressed

OVERSAMPLING = 2

global hWnd2

def wndProc(hWnd, msg, wParam, lParam):
    global render
    global mouse_pressed
    global hWnd2

    if msg == WM_DESTROY:

        PostQuitMessage(0)

        return 0

    if msg == WM_PAINT:

        render.Render()

        #SwapBuffers(GetDC(hWnd))

        x,y,width, height = GetClientRect(hWnd2)

        glReadBuffer(GL_FRONT)

        data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (width, height), data)
        image = ImageOps.flip(image)

        width /= OVERSAMPLING
        height /= OVERSAMPLING

        image = image.resize((width, height), Image.ANTIALIAS)

        hdc, paintstruct = BeginPaint(hWnd)
        dib = ImageWin.Dib(image)
        dib.draw(hdc, (0,0, width, height))

        EndPaint(hWnd, paintstruct)

        return 0

    if msg == WM_SIZE:

        x,y,width,height = GetClientRect(hWnd)
        width *= OVERSAMPLING
        height *= OVERSAMPLING

        # resize render window
        SetWindowPos(hWnd2, None, 0, 0, width, height, 0)

        x,y,width,height = GetClientRect(hWnd2)
        render.ResizeViewport(width, height)

        InvalidateRect(hWnd, None, FALSE)

        return 0

    if msg == WM_LBUTTONDOWN:
        mouse_pressed = ( LOWORD(lParam), HIWORD(lParam) )
        SetCapture(hWnd)
        return 0

    if msg == WM_LBUTTONUP:
        mouse_pressed = ( -1, -1 )
        ReleaseCapture()
        return 0

    if msg == WM_MOUSEMOVE:
        xold, yold = mouse_pressed

        if xold != -1:
            x = LOWORD(lParam)
            y = HIWORD(lParam)
            sens = 0.5
            render.RotateView(sens*(x-xold), sens*(y-yold))
            InvalidateRect(hWnd, None, FALSE)
            mouse_pressed = (x,y)

        return 0

    return DefWindowProc(hWnd, msg, wParam, lParam)
# =========================================

def main():

    global mouse_pressed
    mouse_pressed = (-1,-1)

    hWnd = CreateWindowA(wndProc, "OpenGL Window WGL AA")

    x,y, width, height = GetClientRect(hWnd)
    width *= OVERSAMPLING
    height *= OVERSAMPLING

    # Create invisible window to render to
    global hWnd2
    hWnd2 = CreateWindowA(style = WS_POPUP)

    CreateContext(hWnd2, doubleBuffer=False)

    # window created w/o border and title, so size is same as ClientRect,
    # so actually no need to call GetClientRect
    x,y, width, height = GetClientRect(hWnd2)

    global render
    render = SceneRenderer(width, height)

    ShowWindow(hWnd, True)
    UpdateWindow(hWnd)
    PumpMessages()

    DeleteContext()

main()