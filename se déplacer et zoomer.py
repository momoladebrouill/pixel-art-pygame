import pygame as pg
import time
import random
import math
from colorsys import hsv_to_rgb
from tkinter.filedialog import asksaveasfile
"""à alléger et clarifier"""
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
nbs=10 #le nombre de celules sur la grid
nbsx,nbsy=nbs,nbs
SIZE = WIND/nbs #la taille des cellules

fps = pg.time.Clock()


class dep:
    x=0
    y=0
    sped=-10
    def __repr__(self):
        return str((self.x,self.y))

def find(x,y):return bool(lieux.get((x,y),0))

lieux={}
b = True
mode=''
ct=0
sel=0
depx,depy=0,0
try:
    pg.init()
    click=pg.mixer.Sound('click.ogg')
    switch=pg.mixer.Sound('timer.mp3')
    empty=pg.mixer.Sound('bubbles.mp3')
    f = pg.display.set_mode((0,0))
    pg.display.set_caption("crédit @ryanair aka soldat µ")
    pg.display.init()
    re=pg.display.get_surface().get_rect()
    WINDX=re.width
    WINDY=re.height
    nbsx=int(WINDX/SIZE)
    nbsy=int(WINDY/SIZE)
    font=pg.font.SysFont('consolas',25,1)
    fakeSIZE=75
    while b:
        b+=1
        pg.display.flip()
        si = pg.key.get_pressed()  # SI la touche est appuyée
        if si[pg.K_q]:depx-=dep.sped
        if si[pg.K_s]:depy+=dep.sped
        if si[pg.K_d]:depx+=dep.sped
        if si[pg.K_z]:depy-=dep.sped
        dep.x+=(depx-dep.x)/7
        dep.y+=(depy-dep.y)/7
        for event in pg.event.get():  # QUAND la touche est appuyée

            if event.type == pg.QUIT:
                b = False
                print(" Il y avait {0} cellules".format(len(lieux)))
            if event.type == pg.KEYDOWN:
                touche=event.key
                nbsx=int(WINDX/SIZE)
                nbsy=int(WINDY/SIZE)
                if touche == pg.K_a:
                    for i in range(nbsx):
                        for j in range(nbsy):
                            lieux[(int(-depx/SIZE)+i+0.5,int(-depy/SIZE)+j+0.5)]=0xffffff
                elif touche == pg.K_e:
                    lieux={}
                    empty.play()
                elif touche ==pg.K_r:
                    for i,j in lieux:
                        if i>-depx/SIZE-1 and j>-depy/SIZE-1 and i<-depx/SIZE+nbsx and j<-depy/SIZE+nbsy: # si on a besoin de le dessiner
                            pg.draw.rect(f,lieux[(i,j)],((dep.x+i*SIZE,dep.y+j*SIZE),(SIZE,SIZE)))
                    file=asksaveasfile(defaultextension=".png")
                    if file:
                        lieu=file.name
                        file.close()
                        pg.image.save(f,lieu)
                elif touche == pg.K_ESCAPE:
                    b = False
                    print(" Il y avait {0} cellules".format(len(lieux)))
                    
            elif event.type ==pg.MOUSEBUTTONDOWN:
                if event.button==1:mode='c'
                elif event.button==3:mode='e'
            elif event.type == pg.MOUSEBUTTONUP:
                mode=''

                if event.button==4:
                    fakeSIZE+=5
                    depx-=x*5
                    depy-=y*5
                elif event.button==5:
                    fakeSIZE-=5
                    if SIZE<=0:
                        fakeSIZE=1
                    else:
                        depx+=x*5
                        depy+=y*5
                elif event.button==6:
                    sel-=0.1
                    switch.play()
                elif event.button==7:
                    sel+=0.1
                    switch.play()
                sel=sel%1
                nbsx=int(WINDX/SIZE)
                nbsy=int(WINDY/SIZE)
        SIZE+=(fakeSIZE-SIZE)/7
        x,y=pg.mouse.get_pos()
        x=round((x-depx)/SIZE)-0.5
        y=round((y-depy)/SIZE)-0.5
        
        if mode=='c':
            if lieux.get((x,y),0)!=hsv_to_rgb(sel,1,255):
                click.set_volume(0.5)
                click.play()
            lieux[(x,y)]=hsv_to_rgb(sel,1,255)
            
        elif mode=='e':
            if lieux.get((x,y),False):
                lieux.pop((x,y))
                click.set_volume(1)
                click.play()
        
        f.fill(0)
        for i,j in lieux:
            if i>-depx/SIZE-1 and j>-depy/SIZE-1 and i<-depx/SIZE+nbsx and j<-depy/SIZE+nbsy: # si on a besoin de le dessiner
                pg.draw.rect(f,lieux[(i,j)],((dep.x+i*SIZE,dep.y+j*SIZE),(SIZE,SIZE)))
        pg.draw.rect(f,hsv_to_rgb(sel,1,255),((x*SIZE+dep.x,y*SIZE+dep.y),(SIZE,SIZE)))
        pg.draw.rect(f,0,((x*SIZE+dep.x,y*SIZE+dep.y),(SIZE,SIZE)),width=3)

        fps.tick(FPS)
##        f.blit(font.render(str(sel),10,(0,255,0)),(0,0))
##        f.blit(font.render(str({'x':x,'y':y,'size':SIZE}),10,(0,255,0)),(0,20))
        
        
except:
    pg.quit()
    raise
pg.quit()
