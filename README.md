# PyOpenGL_Examples_SaveToFile
Several examples of how to use PyOpenGL for off-screen rendering and saving rendered image to file. 3 methods are used: using GLUT hidden window, using WGL to create context with default buffer, as well as creation of OpenGL Framebuffer Object by hands and display results with anti-aliasing in the interactive window .

**Important! PyOpenGL 3.1.1 have a bug!**

When you just import WGL, glReadPixels() starts to crash with

ctypes.ArgumentError: argument 7: : wrong type

Go to [package dir]\OpenGL\raw\WGL_types.py , find the following lines

```python
HANDLE = POINTER(None)  # /home/mcfletch/pylive/OpenGL-ctypes/src/wgl.h:60
# TODO: figure out how to make the handle not appear as a void_p within the code...
HANDLE.final = True
```

replace by

```python
HANDLE = UINT64 # for x64, UINT32 for x86
HANDLE.final = True
```

=======
### OpenGL_Offscreen_FBO.py
Offscreen rendering using manually created OpenGL Framebuffer Object

### OpenGL_Offscreen_FBO_standalone.py
Offscreen rendering using manually created OpenGL Framebuffer Object
Standalone code - not using LibGL from this repository

### OpenGL_Offscreen_GLUT.py
Offscreen rendering using GLUT hidden window

### OpenGL_Offscreen_GLUT_standalone.py
Offscreen rendering using GLUT hidden window
Standalone code - not using LibGL from this repository

### OpenGL_Offscreen_WGL.py
Offscreen rendering using WGL default buffers with hidden window

### OpenGL_Offscreen_WGL_standalone.py
Offscreen rendering using WGL default buffers with hidden window
Standalone code - not using LibGL from this repository

### OpenGL_Window_FBO_AA.py
Render using manually created OpenGL Framebuffer Object
Then resize rendered image with anti-aliasing and display it in the window
Use mouse to rotate the view

### OpenGL_Window_GLUT.py
Simple GLUT-based init and double-buffered OpenGL rendering
Use keys to rotate the view

### OpenGL_Window_Simple.py
Standard double-buffered OpenGL rendering
Using WGL SwapBuffers() to show rendered result in the main window
Use mouse to rotate the view

### OpenGL_Window_WGL_AA.py
Render using default WGL buffers in the second hidden window
Then resize rendered image with anti-aliasing and display it in the window
Use mouse to rotate the view
