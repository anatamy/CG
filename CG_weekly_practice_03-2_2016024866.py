#--import part
import glfw
from OpenGL.GL import *
import numpy as np
#-- rendering part
def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()
#-- main part
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_03-2_2016024866", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        # get the current time, in seconds
        t = glfw.get_time() #make random variables
        R = np.array([[np.cos(t), -np.sin(t),0.],[np.sin(t),np.cos(t),0.],[0.,0.,1.]]) #for rotation, rotaion matrix
        T = np.array([[1.,0.,.4], # for translation "moving matrx" for transition
                     [0.,1.,.1],
                     [0.,0.,1.]])
        render(R@T) # rander transition after rotate
        glfw.swap_buffers(window)
    glfw.terminate()
main()
