"""
Kilder:
bane av 徽锦, hentet fra https://pngtree.com/freepng/black-rugged-track-clip-art_5899635.html
bil1, bil2, mållinje av Virgate Designs, hentet fra https://opengameart.org/content/lap-rusher-assets
gress fra tech With Tim, hentet fra https://www.youtube.com/watch?v=L3ktUWfAMPg&t=124s

kode_inspirasjon av Tech with tim, video: Pygame Car Racing Tutorial #1 - Moving The Car, https://www.youtube.com/watch?v=L3ktUWfAMPg&t=124s
og Pygame Car Racing Tutorial #2 - Pixel Perfect Collision, hentet frahttps://www.youtube.com/watch?v=WfqXcyF0_b0

kode om nedtelling av sloth, hentet fra https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame



"""

import pygame as pg
import time
import math

pg.init()
clock = pg.time.Clock()


pg.font.init()

#konstanter
WIDTH = 600
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60

antall_runder = 3



#farger
white = (255, 255, 255)
black = (0, 0, 0)
RED = (255, 0, 0)

font = pg.font.SysFont("comicsans", 44)
font2 = pg.font.SysFont("comicsans", 15)


#funksjon for å endre størelse på bildene
def scale_image(img, storrelse):
    size = round(img.get_width() * storrelse), round(img.get_height() * storrelse)
    return pg.transform.scale(img, size)

#teksten jeg bruker på forsiden
def tekst(surface, font, text):
    render = font.render(text, 1, (white))
    surface.blit(render, (WIDTH/2 - render.get_width()/2, HEIGHT/ 2 - render.get_height()/2))
    
   

#def startside1():
    #return text(surface, font, "press 1 for singel player or 2 for 2 player")

#hvis jeg vil ha to spill muligheter
    
#bliter teksten på framsida   
def startside():
    return tekst(surface, font, "press any key to start")




#filer + masks
bane = scale_image(pg.image.load("bane2.png"), 0.5)

#bane_mask = pg.mask.from_surface(bane)
bane_outline = scale_image(pg.image.load('bane_outline.png'), 0.5)
bane_outline_mask = pg.mask.from_surface(bane_outline)

bil1 = scale_image(pg.image.load('bil1.png'), 0.02)
bil1_mask = pg.mask.from_surface(bil1)

bil2 = scale_image(pg.image.load('bil2.png'), 0.35)
bil2_mask = pg.mask.from_surface(bil2)

finish = scale_image(pg.image.load('finish.png'), 0.5)
finish = pg.transform.rotate(finish, 95)
finish_mask = pg.mask.from_surface(finish)
finish_posisjon = (180, 30 - finish.get_height())

gress = scale_image(pg.image.load('gress.png'), 2)

#poisjon til 
finish_h = finish.get_height()
finish_w = finish.get_width()
finish_x = 180
finish_y = 30

#lyd
motorlyd = pg.mixer.Sound("billyd.ogg")



#bil_bredde = bil1.get_width()
#bil_lengde = bil1.get_height()



#funkjson får å få firkanten til å svinge, slik at fronten til bilen alltid peker i retningen til bevegelsen
def rotasjon(surface, bil, top_left, vinkel):
    
    rotert_bilde = pg.transform.rotate (bil, vinkel)
    #roterer venstre topp hjørne
    new_rect = rotert_bilde.get_rect(center = bil.get_rect(topleft = top_left).center)
    #vil heller at den rotere fra midten av bilde, samtidig som y og x forblir den samme
    #sentrum av bilde forblir sentrum for det rterte bilde 
 
    surface.blit(rotert_bilde, new_rect.topleft)


    
#klasse biler
class Bil:
    def __init__(self, max_vel, rotation_vel,):#maksfart, og rotasjons fart
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.vinkel = 0
        self.x = self.start_posisjonx
        self.y = self.start_posisjony
        self.a = 0.1
        self.mask = pg.mask.from_surface(self.img)
        self.runde = 1
        self.cooldown_tracker = 2000
        
        
    def rotasjon(self, left=False, right=True):
        if left:
            self.vinkel += self.rotation_vel
        elif right:
                self.vinkel -= self.rotation_vel
    
    def draw(self, surface):
        rotasjon(surface, self.img, (self.x, self.y), self.vinkel)
        
    def bevegelse_fremover(self):
        self.vel = min(self.vel + self.a, self.max_vel)
        self.move()


    def move(self):
        radians = math.radians(self.vinkel)
        vertikal = math.sin(radians) * self.vel
        horisontal = math.cos(radians) * self.vel
        
        self.y -= vertikal
        self.x += horisontal
        
    def sakne_ned(self):
        self.vel = max(self.vel - self.a /2, 0)
        self.move()
        
    def kollisjon(self, mask, x=0, y=0):
        car_mask = pg.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y)) 
                                                                                                                    
                                                                                                                                                               
        #gjør om så det kan funke på begge biler 
        kollisjon = mask.overlap(car_mask, offset)
        return kollisjon
    

    
        
class Spiller1(Bil):
    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)

    IMG = bil1
    start_posisjonx = 200
    start_posisjony = 60
    moved = False
    
    

    
    def kreasj(self):
        self.vel = -self.vel
    
    def bevegelse_av_bil(self):
        keys = pg.key.get_pressed()
        moved = False
        
        if keys[pg.K_LEFT]:
            self.rotasjon(left = True)
        if keys[pg.K_RIGHT]:
            self.rotasjon(right = True)
        if keys[pg.K_UP]:
            self.bevegelse_fremover()
            motorlyd.play()
            moved = True
            self.bevegelse_fremover()
            
        if not moved:
            self.sakne_ned()
        
   
    
    
          
class Spiller2(Bil):
    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        
        
    IMG = bil2
    start_posisjonx = 200
    start_posisjony = 35
    
    
    def kreasj(self):
        self.vel = -self.vel
        
    def bevegelse_av_bil(self):
        keys = pg.key.get_pressed()
        moved = False
    
        if keys[pg.K_a]:
            self.rotasjon(left = True)
        if keys[pg.K_d]:
            self.rotasjon(right = True)
        if keys[pg.K_w]:
            self.bevegelse_fremover()
            moved = True
            #self.bevegelse_fremover()
            
        if not moved:
            self.sakne_ned()
        
        

   
#cooldown_tracker = 2000


def kollisjon_med_mållinja(spiller1, spiller2):
    #global cooldown_tracker
    
    spiller1.cooldown_tracker += clock.get_time()

    
    if spiller1.y + bil1.get_height() <= finish_y + finish_h and spiller1.x + bil1.get_width() >= finish_x and spiller1.x + bil1.get_width() < finish_x + finish_w:
        if spiller1.cooldown_tracker > 20000:
            #slik at runde kun øker med en om gangen
            spiller1.runde += 1
            spiller1.cooldown_tracker = 0

        
        
    runde_text = font2.render(f"Runde spiller1: {spiller1.runde}/3", 1, black)
    surface.blit(runde_text, (50, 565))
        
       
    spiller2.cooldown_tracker += clock.get_time()

    if spiller2.y + bil2.get_height() <= finish_y + finish_h and spiller2.x + bil2.get_width() >= finish_x and spiller2.x + bil2.get_width() < finish_x + finish_w:
        if spiller2.cooldown_tracker > 20000:
            spiller2.runde += 1
            spiller2.cooldown_tracker = 0
            
    runde_text = font2.render(f"Runde spiller2: {spiller2.runde}/3", 1, black)
    surface.blit(runde_text, (450, 565))



def vinner(spiller1, spiller2):
    if spiller1.runde >= antall_runder + 1:
        tekst(surface, font, "Rød bil vinner!!!")
        spiller1.max_vel = 0
        spiller2.max_vel = 0
    if spiller2.runde >= antall_runder + 1:
        tekst(surface, font, "Blå bil vinner!!!")
        spiller1.max_vel = 0
        spiller2.max_vel = 0
        
"""
fosøk på kollisjon mellom bilene ved bruk av sprite.collide


def kollisjon_mellom_bilene(spiller1, spiller2):
    kollisjon = pg.sprite.collide_rect(spiller1, spiller2)
    if kollisjon == True:
        spiller1.kreasj()
        spiller2.kreasj()
    
"""


#konstanter til nedtellingen
teller = 4
text = '4' .rjust(3)
pg.time.set_timer(pg.USEREVENT, 1000)

  
"""
def draw2(surface, img, spiller, pos):
    
    #surface.blit(img, pos)
    
    
    
    spiller.draw(surface)
    pg.display.update()
"""

                

#lager vindu



spiller1 = Spiller1(3, 3)
spiller2 = Spiller2(3, 3  )
surface = pg.display.set_mode(SIZE)

run = True
#nytt_poeng = False
start = True




while run:
    clock.tick(FPS)
    molstrek = True
        
    #startside
    while start == True:
       surface.fill(black)
       startside()
       pg.display.update()
       for event in pg.event.get():
           
           if event.type == pg.QUIT:
               start = False
               break
           if event.type == pg.KEYDOWN:
                start = False
                nedtelling = True
           break
    
    #nedtelling
    while nedtelling:
        for event in pg.event.get():
            if event.type == pg.USEREVENT:
                teller -= 1
                text = str(teller).rjust(3)
                surface.fill(black)
                #surface.blit(font.render(text, True, white), (32, 48))
                tekst(surface, font, text)
                pg.display.update()
            if event.type == pg.QUIT:
                nedtelling = False
                break
            if teller == 0:
                nedtelling = False
                

        #surface.fill(black)
        #surface.blit(font.render(text, True, white), (32, 48)) #bytt til funksjon
        #pg.display.update()
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        
        
        
#sett dette inn i i en klasse
        
    
    
    #overfører filer til spill
    surface.blit(gress, (0, 0))
    surface.blit(bane, (0, 0))
    surface.blit(finish, (180, 30))
    
    #tegner biler
    spiller1.draw(surface)
    spiller2.draw(surface)
    
    #surface.blit(bil1, (140, 40 ))
    #surface.blit(bil2, (140, 75))
    
    
    spiller1.bevegelse_av_bil()
    spiller2.bevegelse_av_bil()
   
    

    
    
#kollisjon med siden av banen
    
    if spiller1.kollisjon(bane_outline_mask) != None:
        spiller1.kreasj()
        
    if spiller2.kollisjon(bane_outline_mask) != None:
        spiller2.kreasj()

#kollisjon med motsatt bil eller i hvert fall et forsøk
    if spiller1.kollisjon(spiller2.mask) or spiller2.kollisjon(spiller1.mask) != None:
        spiller1.kreasj()
        spiller2.kreasj()


    kollisjon_med_mållinja(spiller1, spiller2)
    vinner(spiller1, spiller2)  

    

    fart_text = font2.render(f"fart spiller 1: {round(spiller1.vel)} px/s", 1, black)
    surface.blit(fart_text, (50, 550))
    
    fart_text = font2.render(f"fart spiller 2: {round(spiller2.vel)} px/s", 1, black)
    surface.blit(fart_text, (450, 550))
    

    
    pg.display.update()
    pg.display.flip()
    
 
    
pg.quit()


