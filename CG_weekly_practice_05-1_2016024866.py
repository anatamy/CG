import glfw
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pdb

def drawUnitCube():
  glBegin(GL_QUADS)
  glVertex3f( 0.5, 0.5,-0.5)
  glVertex3f(-0.5, 0.5,-0.5)
  glVertex3f(-0.5, 0.5, 0.5)
  glVertex3f( 0.5, 0.5, 0.5)
  glVertex3f( 0.5,-0.5, 0.5)
  glVertex3f(-0.5,-0.5, 0.5)
  glVertex3f(-0.5,-0.5,-0.5)
  glVertex3f( 0.5,-0.5,-0.5)
  glVertex3f( 0.5, 0.5, 0.5)
  glVertex3f(-0.5, 0.5, 0.5)
  glVertex3f(-0.5,-0.5, 0.5)
  glVertex3f( 0.5,-0.5, 0.5)
  glVertex3f( 0.5,-0.5,-0.5)
  glVertex3f(-0.5,-0.5,-0.5)
  glVertex3f(-0.5, 0.5,-0.5)
  glVertex3f( 0.5, 0.5,-0.5)
  glVertex3f(-0.5, 0.5, 0.5)
  glVertex3f(-0.5, 0.5,-0.5)
  glVertex3f(-0.5,-0.5,-0.5)
  glVertex3f(-0.5,-0.5, 0.5)
  glVertex3f( 0.5, 0.5,-0.5)
  glVertex3f( 0.5, 0.5, 0.5)
  glVertex3f( 0.5,-0.5, 0.5)
  glVertex3f( 0.5,-0.5,-0.5)
  glEnd()

def drawCubeArray():
  for i in range(5):
    for j in range(5):
      for k in range(5):
        glPushMatrix()
        glTranslatef(i,j,-k-1)
        glScalef(.5,.5,.5)
        drawUnitCube()
        glPopMatrix()

def drawFrame():
  glBegin(GL_LINES)
  glColor3ub(255, 0, 0)
  glVertex3fv(np.array([0.,0.,0.]))
  glVertex3fv(np.array([1.,0.,0.]))
  glColor3ub(0, 255, 0)
  glVertex3fv(np.array([0.,0.,0.]))
  glVertex3fv(np.array([0.,1.,0.]))
  glColor3ub(0, 0, 255)
  glVertex3fv(np.array([0.,0.,0]))
  glVertex3fv(np.array([0.,0.,1.]))
  glEnd()

def render():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
  glLoadIdentity()
  myOrtho(-5,5, -5,5, -8,8)
  myLookAt(np.array([5,3,5]), np.array([1,1,-1]), np.array([0,1,0]))
  # Above two lines must behaves exactly same as the below two lines
  # glOrtho(-5,5, -5,5, -8,8)
  # gluLookAt(5,3,5, 1,1,-1, 0,1,0)
  drawFrame()
  glColor3ub(255, 255, 255)
  drawCubeArray()

def normalize(vec):
  new_vec  = vec / np.sqrt(np.sum(vec**2))
  return new_vec

# def myOrtho(left, right, bottom, top, near, far):
# implement here
def myLookAt(eye,at,up):
  forward =(eye-at)
  n_forward=normalize(forward)
  # n_forward=(eye-at) / np.sqrt(np.dot(eye-at,eye-at))
  side=np.cross(up,n_forward)
  n_side=normalize(side)
  # n_side=np.cross(up, n_forward) / np.sqrt(np.dot(np.cross(up, n_forward), np.cross(up, n_forward)))
  n_up = np.cross(n_forward,n_side)
  pos=np.array([sum(-eye*n_side), sum(-eye*n_up) ,sum(-eye*n_forward)])
  # m_pos=np.array([-n_side @ eye,-n_up @ eye,-n_forward@eye])
  # pdb.set_trace()
  M=np.array([
  [n_side[0],n_up[0],n_forward[0],0.],
  [n_side[1],n_up[1],n_forward[1],0.],
  [n_side[2],n_up[2],n_forward[2],0.],
  [pos[0],pos[1],pos[2],1.]
  ])
  # pdb.set_trace()
  glMultMatrixf(M)
def myOrtho(left,right,bottom,top,near,far):
  M=np.array([
  [2./(right-left),0.,0.,-((right+left)/(right-left))],
  [0.,2./(top-bottom),0.,-((top+bottom)/(top-bottom))],
  [0.,0.,2./(near-far),-((near+far)/(far-near))],
  [0.,0.,0.,1.]
  ])
  # pdb.set_trace()
  glMultMatrixf(M.T)
# def myLookAt(eye, at, up):
# implement here

def main():
  # pdb.set_trace()
  if not glfw.init():
    return
  window = glfw.create_window(480,480,'CG_weekly_practice_05-1_2016024866',None,None)
  if not window:
    glfw.terminate()
    return
  glfw.make_context_current(window)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    render()
    glfw.swap_buffers(window)
  glfw.terminate()


if __name__=="__main__":
  main()
