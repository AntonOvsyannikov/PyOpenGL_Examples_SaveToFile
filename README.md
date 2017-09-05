## PyOpenGL_Examples_SaveToFile
Several examples of how to use PyOpenGL for off-screen rendering and saving rendered image to file. 3 methods are used: using GLUT hidden window, using WGL to create context with default buffer, as well as creation of OpenGL Framebuffer Object by hands and display results with anti-aliasing in the interactive window .

**Important! PyOpenGL 3.1.1 have a bug!**

When you just import WGL, glReadPixels() starts to crash with

ctypes.ArgumentError: argument 7: : wrong type

Go to [package dir]\OpenGL\raw\WGL_types.py , find the following lines

'''python
HANDLE = POINTER(None)  # /home/mcfletch/pylive/OpenGL-ctypes/src/wgl.h:60
# TODO: figure out how to make the handle not appear as a void_p within the code...
HANDLE.final = True
'''

replace by

'''python
HANDLE = UINT64 # for x64, UINT32 for x86
HANDLE.final = True
'''

