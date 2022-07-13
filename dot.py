from structure import Renderer, color
import random

width = 1024
height = 600

rend = Renderer(width, height) # Los parámetros son pixeles.

# Rend de viewport
rend.glViewport(int(width/4), 
                int(height/4),
                int(width/2),
                int(height/2))
rend.glClearViewport(color(1,0,0))
rend.glClearColor(1,1,1)
rend.glClear()
rend.glClearViewport(color(0.9,0.9,0.9))

rend.glPoint_vp(0,0,color(0,0,1))
rend.glPoint_vp(1,1,color(0,1,0))
rend.glPoint_vp(-1,-1,color(1,0,0))


rend.glFinish('output.bmp')


