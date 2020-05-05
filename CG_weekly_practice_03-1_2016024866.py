# import part
import glfw
from OpenGL.GL import *
import numpy as np

# define glbal variables
val_position=np.linspace(0,330,12) #0,30,60 .... 330
val_mode=GL_LINE_LOOP #glbegin mode value

# handler of key event 1~0
def key_callback(window, key, scancode, action, mods):
    global val_mode #we should do this
    if (key==glfw.KEY_1 and action==glfw.PRESS):
        val_mode=GL_POINTS
    elif (key==glfw.KEY_2 and action==glfw.PRESS):
        val_mode=GL_LINES
    elif (key==glfw.KEY_3 and action==glfw.PRESS):
        val_mode=GL_LINE_STRIP
    elif (key==glfw.KEY_4 and action==glfw.PRESS):
        val_mode=GL_LINE_LOOP
    elif (key==glfw.KEY_5 and action==glfw.PRESS):
        val_mode=GL_TRIANGLES
    elif (key==glfw.KEY_6 and action==glfw.PRESS):
        val_mode=GL_TRIANGLE_STRIP
    elif (key==glfw.KEY_7 and action==glfw.PRESS):
        val_mode=GL_TRIANGLE_FAN
    elif (key==glfw.KEY_8 and action==glfw.PRESS):
        val_mode=GL_QUADS
    elif (key==glfw.KEY_9 and action==glfw.PRESS):
        val_mode=GL_QUAD_STRIP
    elif (key==glfw.KEY_0 and action==glfw.PRESS):
        val_mode=GL_POLYGON

# rendering part
def render():
    global val_mode
    global val_position
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glBegin(val_mode)
    for i in val_position: #make verteces by repeat
        glVertex2f(np.cos(round(i*np.pi / 180.,2)),np.sin(round(i*np.pi/180.,2))) # i is radian so we should convert it
    glEnd()
    glFlush()

def main():
    global val_mode
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_03-1_2016024866",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1) 
    while not glfw.window_should_close(window):
        glfw.wait_events()
        glfw.set_key_callback(window,key_callback) #key evenet handler
        render()
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__=="__main__":
    main()
