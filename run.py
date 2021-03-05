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
viewport = (1280,720)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF |pygame.RESIZABLE)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)

global specref
specref = (1.0, 1.0, 1.0, 1.0)

glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
glMateriali(GL_FRONT, GL_SHININESS, 128)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
objBall = OBJ('ballVM.obj', swapyz=False)

objCannon = OBJ('cannonVM.obj', swapyz=False)
objWheel = OBJ('walllVM.obj', swapyz=False)
##objFloor = OBJ('plane.obj', swapyz=False)
##objFire = OBJ('fire.obj', swapyz=False)
##

objCannon.generate()
objBall.generate()
objWheel.generate()
##objFloor.generate()
##objFire.generate()



clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)

glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
ypos = 5

rotate = move = False
running = True
while running:
    clock.tick(30)
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT:
            running  = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            running  = False
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
  
    

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
                zpos -=1
    elif keys_pressed[pygame.K_DOWN]:
                zpos +=1

    elif keys_pressed[pygame.K_RIGHT]:
                tx -=1
    elif keys_pressed[pygame.K_LEFT]:
                tx +=1
    elif keys_pressed[pygame.K_a]:
                glPushMatrix()
                glTranslate(rx,ry,90)
                objWheel.render()
                glPopMatrix()
                glLoadIdentity()

    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glLoadIdentity()


    lightPos = (-50.0, 50.0, 100.0, 1.0)
    # RENDER OBJECT
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    objCannon.render()
##    objFloor.render()
    objWheel.render()
    objBall.render()


    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)


##    objFire.render()


    
    pygame.display.flip()
##    pygame.display.update()
pygame.quit()
