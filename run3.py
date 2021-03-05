#!/usr/bin/env python
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from objloader3 import *

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
objBall = OBJ('ball.obj', swapyz=False)

objCannon = OBJ('cannonMain.obj', swapyz=False)
objWheel = OBJ('wheel.obj', swapyz=False)
objFloor = OBJ('plane.obj', swapyz=False)

objCannon.generate()
objBall.generate()
objWheel.generate()
objFloor.generate()



clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False
def keyboard(key, x, y):
    print("Keyboard fuction active")
    global anim
    if key == chr(27):
        sys.exit()
    if key == b'a':
        anim = 1
    if key == b's':
        anim = 0
    if key == b'q':
        sys.exit()
while 1:
  

    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j


##
##    keys_pressed = pygame.key.get_pressed()
##    if keys_pressed[pygame.K_UP]:
##        glPushMatrix()
##        glTranslate(0,5,-10)
##        objWheel.render()
##        glPopMatrix()
##
##    if keys_pressed[pygame.K_DOWN]:
##        glPushMatrix()
##        glTranslate(0,5,-10)
##        objCannon.render()
##        glPopMatrix()

    glLoadIdentity()

    # RENDER OBJECT
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    objCannon.render()
    objFloor.render()
    objWheel.render()

    glPushMatrix()
    glTranslate(0,5,-10)
    objBall.render()
    
    glPopMatrix()

    pygame.display.flip()
