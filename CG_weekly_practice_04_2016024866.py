# import part
import glfw
from OpenGL.GL import *
import numpy as np


# define glbal variables
val_degree=0
val_translate=0
val_switch=0
val_scale=1
S=np.array([[val_scale,0.,0.],

            [0.,1.,0.],
            [0.,0.,1.]])
T=np.array([[1,0.,0.],
            [0.,1.,0.],
            [0.,0.,1.]])
val_T=T
print(val_T)

def key_callback(window, key, scancode, action, mods):
    global T
    global val_T
    #Translate by -0.1 in x direction w.r.t global coordinate
    if (key==glfw.KEY_Q and action==glfw.PRESS):
        T[0,2]=-0.1
        val_T=T @ val_T
        T[0,2]=0
    #Translate by 0.1 in x direction w.r.t global coordinate
    elif (key==glfw.KEY_E and action==glfw.PRESS):
        T[0,2]=0.1
        val_T= T @ val_T
        T[0,2]=0
    elif (key==glfw.KEY_2 and action==glfw.PRESS):
        T[0,2]=-0.1
        val_T= val_T @T
        T[0,2]=0
    elif (key==glfw.KEY_3 and action==glfw.PRESS):
        T[0,2]=0.1
        val_T= val_T @ T
        T[0,2]=0
    #Rotate by 10 degrees counterclockwise w.r.t local coordinate
    elif (key==glfw.KEY_A and action==glfw.PRESS):
        th=10*np.pi/180
        R= np.array([[np.cos(th),-np.sin(th),0],
                    [np.sin(th), np.cos(th),0],
                    [0.,0.,1.]])
        val_T= val_T @ R
    #Rotate by 10 degrees clockwise w.r.t local coordinate
    elif (key==glfw.KEY_D and action==glfw.PRESS):
        th=-10*np.pi/180
        R= np.array([[np.cos(th),-np.sin(th),0],
                    [np.sin(th), np.cos(th),0],
                    [0.,0.,1.]])
        val_T= val_T @ R
    #Reset the triangle with identity matrix
    elif (key==glfw.KEY_1 and action==glfw.PRESS):
        val_T=np.identity(3)
    #Scale by 0.9 times in x direction w.r.t global coordinate
    elif (key==glfw.KEY_W and action==glfw.PRESS):
        T[0,0]=T[0,0]*0.9
        val_T= T @ val_T
        T[0,0]=1
        print(T)
    #Rotate by 10 degrees counterclockwise w.r.t global coordinate
    elif (key==glfw.KEY_S and action==glfw.PRESS):
        th=10*np.pi/180
        R= np.array([[np.cos(th),-np.sin(th),0],
                    [np.sin(th), np.cos(th),0],
                    [0.,0.,1.]])
        val_T= R @ val_T
    #print(val_T)

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




# identity : 정방단위행렬
# glMultMatrix : multiply the current transformation matrix with the matrix m
# glrotate : multiply the current matrix by a rotation matrix
# glTranslate: multiply the current matrix by a translation matrix
# left-to right => local frame (점변환)
# right to left => world frame (좌표계 변환)
def main():
    global val_degree
    global val_translate
    global val_switch
    global val_scale
    global val_T
    if not glfw.init():
        return
    window=glfw.create_window(480,480,"CG_weekly_practice_04_2016024866",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.wait_events()
        #t=glfw.get_time()
    #rotation part
        #th=np.radians(-60)
        glfw.set_key_callback(window,key_callback)
        # R=np.identity(3)
        # R[:2,:2 ] = [[np.cos(round(val_degree*np.pi/180,2)), -np.sin(round(val_degree*np.pi/180,2))],
        #             [np.sin(round(val_degree*np.pi/180,2)), np.cos(round(val_degree*np.pi/180,2))]]
        # #translate part
        # T=np.identity(3)
        # T[:3,2] = [val_translate,0.,0.]
        # #scale part
        # S=np.identity(3)
        # S[:2,:2] =[[val_scale,0],
        #             [0,1]]
        render(val_T)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__=="__main__":
    main()
