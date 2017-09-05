from PIL import Image
from PIL import ImageWin
from PIL import ImageOps

from SceneRenderer import *

from LibGL.Win32 import *
from LibGL.Context import *
from LibGL.Buffers import *

from win32gui import *

# =========================================

global buffers
global render

global mouse_pressed

OVERSAMPLING = 2

def wndProc(hWnd, msg, wParam, lParam):

    global buffers
    global render
    global mouse_pressed

    if msg == WM_DESTROY:

        PostQuitMessage(0)

        return 0

    if msg == WM_PAINT:

        render.Render()

        data, width, height = ReadColorBuffer(buffers)
        image = Image.frombytes("RGBA", (width, height), data)
        image = ImageOps.flip(image)
        image = image.resize((width/OVERSAMPLING , height/OVERSAMPLING ), Image.ANTIALIAS  )

        hdc, paintstruct = BeginPaint(hWnd)
        dib = ImageWin.Dib(image)
        dib.draw(hdc, (0,0, width/OVERSAMPLING , height/OVERSAMPLING ))

        EndPaint(hWnd, paintstruct)

        return 0

    if msg == WM_SIZE:

        x,y, width, height = GetClientRect(hWnd)
        width *= OVERSAMPLING
        height *= OVERSAMPLING

        DeleteBuffers(buffers)
        buffers = CreateBuffers(width, height)
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

def main():

    global mouse_pressed
    mouse_pressed = (-1,-1)

    hWnd = CreateWindowA(wndProc, "OpenGL Window FBO AA")

    x, y, width, height = GetClientRect(hWnd)

    width *= OVERSAMPLING
    height *= OVERSAMPLING

    CreateContext(hWnd)

    global buffers
    buffers = CreateBuffers(width, height)

    global render
    render = SceneRenderer(width, height)

    ShowWindow(hWnd, True)
    UpdateWindow(hWnd)
    PumpMessages()

    DeleteBuffers(buffers)
    DeleteContext()

main()