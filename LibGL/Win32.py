from win32api import *
from win32con import *
from win32gui import *
import uuid

def CreateWindowA(wndProc = DefWindowProc, title = '', size = (300, 300), style = WS_OVERLAPPEDWINDOW, coords = (CW_USEDEFAULT, CW_USEDEFAULT)):
    sx, sy = size

    hInstance = GetModuleHandle(None)

    wndClass = WNDCLASS()

    wndClass.lpfnWndProc = wndProc
    wndClass.hInstance = hInstance
    wndClass.hbrBackground = GetStockObject(WHITE_BRUSH)
    wndClass.hCursor = LoadCursor(0, IDC_ARROW)
    wndClass.lpszClassName = str(uuid.uuid4())
    wndClass.style = CS_OWNDC

    wndClassAtom = RegisterClass(wndClass)

    return CreateWindow(wndClassAtom, title, style, coords[0], coords[1], size[0], size[1], 0, 0, hInstance, None)
