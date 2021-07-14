import pygame as pg
from colorsys import hsv_to_rgb,rgb_to_hsv
from tkinter.filedialog import asksaveasfile,askopenfile
import json
"""à alléger et clarifier"""






class dep:
    x=0
    y=0
    sped=-10
    def __str__(dep):
        return str((dep.x,dep.y))
dep=dep()
def find(x,y):return bool(lieux.get((x,y),0))
def coul(sel):
    if sel==1: return 0xffffff
    else: return hsv_to_rgb(sel,1,255)
def get_hue(pos):
    rgb=lieux.get((x,y),0)
    if rgb==0xffffff or rgb==0: return 1
    else:return rgb_to_hsv(*rgb)[0]
        
lieux={}
b = True
mode=''
ct=0
sel=0
depx,depy=0,0
developper=False
fakeSIZE=75
si={}
nbs=10 #le nombre de celules sur la grid
nbsx,nbsy=nbs,nbs
SIZE = WIND/nbs #la taille des cellules
try:
    pg.init()
    fps = pg.time.Clock()
    
    f = pg.display.set_mode((0,0))
    pg.display.set_caption("crédit @ryanair aka soldat µ")
    pg.display.init()
    font=pg.font.SysFont('consolas',15,1)
    re=pg.display.get_surface().get_rect()
    WINDX=re.width
    WINDY=re.height
    del re
    nbsx=int(WINDX/SIZE)
    nbsy=int(WINDY/SIZE)
    
    class sound:
        click=pg.mixer.Sound('sonds//click.ogg')
        switch=pg.mixer.Sound('sonds//change.mp3')
        empty=pg.mixer.Sound('sonds//bubbles.mp3')
        white=pg.mixer.Sound('sonds//timer.mp3')
        erase=pg.mixer.Sound('sonds//erase.mp3')
    while b:
        b+=1
        b=b%60
        pg.display.flip()
        if si.get(pg.K_q):depx-=dep.sped
        if si.get(pg.K_s):depy+=dep.sped
        if si.get(pg.K_d):depx+=dep.sped
        if si.get(pg.K_z):depy-=dep.sped
        dep.x+=(depx-dep.x)/7
        dep.y+=(depy-dep.y)/7
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
            elif event.type== pg.KEYUP:
                si[event.key]=False
                if event.key==pg.K_F1:
                    sel-=0.1
                    switch.play()
                elif event.key==pg.K_F2:
                    sel+=0.1
                    switch.play()
                elif event.key==pg.K_F3:
                    dep.x,dep.y=0,0
                elif event.key==pg.K_F4:
                    file=askopenfile()
                    if file:
                        load=json.loads(file.read())
                        for key in load:
                            pt=key.find('.')
                            X=int(key[:pt])
                            Y=int(key[pt+1:])
                            lieux[(X+.5,Y+.5)]=load[key]
                elif event.key==pg.K_F5:
                    developper= not developper
                    
                sel=round(sel,1)%1.2
            if event.type == pg.KEYDOWN:
                touche=event.key
                si[touche]=True
                nbsx=int(WINDX/SIZE)
                nbsy=int(WINDY/SIZE)
                if touche == pg.K_F6:
                    for i in range(nbsx):
                        for j in range(nbsy):
                            lieux[(int(-depx/SIZE)+i+0.5,int(-depy/SIZE)+j+0.5)]=0xffffff
                    white.play()
                elif touche == pg.K_F7:
                    lieux={}
                    empty.play()
                elif touche ==pg.K_F8:
                    for i,j in lieux:
                        if i>-depx/SIZE-1 and j>-depy/SIZE-1 and i<-depx/SIZE+nbsx and j<-depy/SIZE+nbsy: # si on a besoin de le dessiner
                            pg.draw.rect(f,lieux[(i,j)],((dep.x+i*SIZE,dep.y+j*SIZE),(SIZE,SIZE)))
                    file=asksaveasfile(defaultextension=".png")
                    if file:
                        lieu=file.name
                        file.close()
                        print(lieu)
                        pg.image.save(f,lieu)
                        azerty=open(lieu+"pxl","w")
                        save={}
                        for key in lieux:
                            save[float(str(int(key[0]))+'.'+str(int(key[1])))]=lieux[key]
                        azerty.write(json.dumps(save,indent=4))
                        azerty.close()
                elif touche == pg.K_ESCAPE:
                    b = False
                    print(" Il y avait {0} cellules".format(len(lieux)))
                    
            elif event.type ==pg.MOUSEBUTTONDOWN:
                if event.button==1:mode='c'
                elif event.button==2:sel=get_hue((x,y))
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
               
                nbsx=int(WINDX/SIZE)
                nbsy=int(WINDY/SIZE)
        SIZE+=(fakeSIZE-SIZE)/7
        x,y=pg.mouse.get_pos()
        x=round((x-depx)/SIZE)-0.5
        y=round((y-depy)/SIZE)-0.5
        
        if mode=='c':
            if lieux.get((x,y),0)!=coul(sel):
                click.play()
            lieux[(x,y)]=coul(sel)
            
        elif mode=='e':
            if lieux.get((x,y),False):
                lieux.pop((x,y))
                erase.play()
        
        f.fill(0)
        for i,j in lieux:
            if i>-depx/SIZE-2 and j>-depy/SIZE-2 and i<-depx/SIZE+nbsx+1 and j<-depy/SIZE+nbsy+1: # si on a besoin de le dessiner
                pg.draw.rect(f,lieux[(i,j)],((dep.x+i*SIZE,dep.y+j*SIZE),(SIZE,SIZE)))
        pg.draw.rect(f,coul(sel),((x*SIZE+dep.x,y*SIZE+dep.y),(SIZE,SIZE)))
        pg.draw.rect(f,0,((x*SIZE+dep.x,y*SIZE+dep.y),(SIZE,SIZE)),width=3)
        if developper:
            decal=0
            for fed in [elem+' = '+str(eval(elem))[:50] for elem in dir() if not elem.startswith('__')]:
                truc=font.render(fed,1,(255,255,255),0)
                f.blit(truc,(0,decal))
                decal+=truc.get_rect().height
        fps.tick(60)

        
        
except:
    pg.quit()
    raise
pg.quit()
