'''
Standard double-buffered OpenGL rendering
Using WGL SwapBuffers() to show rendered result in the main window
Use mouse to rotate the view
'''

from LibGL.Win32 import *
from LibGL.Context import *

from win32gui import *

from Renderers.Renderer3D import *

# =========================================

global render

global mouse_pressed

def wndProc(hWnd, msg, wParam, lParam):

    global render
    global mouse_pressed

    if msg == WM_DESTROY:

        PostQuitMessage(0)

        return 0

    if msg == WM_PAINT:

        render.Render()
        SwapBuffers(GetDC(hWnd))

        return 0

    if msg == WM_SIZE:

        x,y, width, height = GetClientRect(hWnd)
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

    hWnd = CreateWindowA(wndProc, "Simple OpenGL Window")

    x, y, width, height = GetClientRect(hWnd)

    CreateContext(hWnd)

    global render
    render = SceneRenderer(width, height)

    ShowWindow(hWnd, True)
    UpdateWindow(hWnd)
    PumpMessages()

    DeleteContext()

main()