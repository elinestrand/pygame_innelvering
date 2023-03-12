import pygame as pg
import time
import math
#from funk_til_spill import scale_image, rotasjon, tekst, startside, bevegelse_av_bil1, bevegelse_av_bil2

pg.font.init()

#konstanter
WIDTH = 600
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60



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

def tekst(surface, font, text):
    render = font.render(text, 1, (white))
    surface.blit(render, (WIDTH/2 - render.get_width()/2, HEIGHT/ 2 - render.get_height()/2))

#def startside1():
    #return text(surface, font, "press 1 for singel player or 2 for 2 player")

#hvis jeg vil ha to spill muligheter
    
    
def startside():
    return tekst(surface, font, "press any key to start")
"""
def tegnTekst(tekst, x, y, farge, fontSize):
    # Henter font
    font = pg.font.SysFont("comicsans", fontSize)
    
    # Lager et tekstbilde
    textImg = font.render(tekst, True, farge)
    
    # Henter rektangelet til tekstboksen
    textRect = textImg.get_rect()
    
    # Putter i vinduet
    surface.blit(textImg, (x - textRect.width//2, y - textRect.height//2))
"""
#filer
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

finish_h = finish.get_height()
finish_w = finish.get_width()
finish_x = 180
finish_y = 30

gress = scale_image(pg.image.load('gress.png'), 2)



bil_bredde = bil1.get_width()
bil_lengde = bil1.get_height()



#funkjson får å få firkanten til å rotere, altså bilde skal rotere når du vil at bilen skal svinge
def rotasjon(surface, bil, top_left, vinkel):
    
    rotert_bilde = pg.transform.rotate (bil, vinkel)
    #roterer venstre topp hjørne
    new_rect = rotert_bilde.get_rect(center = bil.get_rect(topleft = top_left).center)
    #vil heller at den rotere fra midten av bilde, samtidig som y og x forblir den samme
    #det er det linjen over gjør
 
    surface.blit(rotert_bilde, new_rect.topleft)


    
#klasse biler
class Bil:
    def __init__(self, max_vel, rotation_vel):#maksfart, og rotasjons fart
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.vinkel = 0
        self.x = self.start_posisjonx
        self.y = self.start_posisjony
        self.a = 0.1
        
        
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
    
    
    IMG = bil1
    start_posisjonx = 200
    start_posisjony = 60
    
    def kreasj(self):
        self.vel = -self.vel
        
    
"""
dette skal funke innen presentasjonen

    def move(self):
        keys = pg.key.get_pressed()
        moved = False
    
        if keys[pg.K_LEFT]:
            self.rotasjon(left = True)
        if keys[pg.K_RIGHT]:
            self.rotasjon(right = True)
        if keys[pg.K_UP]:
            self.bevegelse_fremover()
            moved = True
            self.bevegelse_fremover()
            
        if not moved:
            self.sakne_ned()
"""    
    
    
          
class Spiller2(Bil):
    IMG = bil2
    start_posisjonx = 200
    start_posisjony = 35
    
    def kreasj(self):
        self.vel = -self.vel
"""

samme her

    def move(self):
        keys = pg.key.get_pressed()
        moved = False
        
        if keys[pg.K_a]:
            self.rotasjon(left = True)
        if keys[pg.K_d]:
            self.rotasjon(right = True)
        if keys[pg.K_w]:
            self.bevegelse_fremover()
            moved = True
            self.bevegelse_fremover()
            
        if not moved:
            self.sakne_ned()
            

"""

def bevegelse_av_bil1(spiller):
    
    
    keys = pg.key.get_pressed()
    moved = False
    
    if keys[pg.K_LEFT]:
        spiller.rotasjon(left = True)
    if keys[pg.K_RIGHT]:
        spiller.rotasjon(right = True)
    if keys[pg.K_UP]:
        spiller.bevegelse_fremover()
        moved = True
        spiller.bevegelse_fremover()
        
    if not moved:
        spiller.sakne_ned()
        
def bevegelse_av_bil2(spiller):
    keys = pg.key.get_pressed()
    moved = False
    
    if keys[pg.K_a]:
        spiller.rotasjon(left = True)
    if keys[pg.K_d]:
        spiller.rotasjon(right = True)
    if keys[pg.K_w]:
        spiller.bevegelse_fremover()
        moved = True
        spiller.bevegelse_fremover()
        
    if not moved:
        spiller.sakne_ned()

  
runde_spiller1 = 1
runde_spiller2 = 1

def kollisjon_med_mållinja(spiller1, spiller2):

    
    if spiller1.y + bil1.get_height() <= finish_y + finish_h and spiller1.x + bil1.get_width() >= finish_x and spiller1.x + bil1.get_width() < finish_x + finish_w:
        tekst(surface, font, "Rød bil vinner!!!")
        #runde_spiller1 += 1
        #return runde_spiller1
        

    if spiller2.y + bil2.get_height() <= finish_y + finish_h and spiller2.x + bil2.get_width() >= finish_x and spiller2.x + bil2.get_width() < finish_x + finish_w:
        tekst(surface, font, "Blå bil vinner!!!")
        #runde_spiller2 += 1
        #return runde_spiller2
"""        
        
def runder(maksrunder, spiller1, spiller2):
    if runde_spiller1 >= maksrunder:
        tekst(surface, font, "Rød bil vinner!!!")
        spiller2.vel = 0
        spiller1.vel = 0
        
    if runde_spiller2 >= maksrunder:
        tekst(surface, font, "Blå bil vinner!!!")
        spiller2.vel = 0
        spiller1.vel = 0


def kollisjon_mellom_biler(spiller1, spiller2, bil1, bil2):
    bil1_v2 = rotert_bilde.get_rect(center = bil1.get_rect(topleft = spiller1.x).center)
    bil2_v2 = rotert_bilde.get_rect(center = bil2.get_rect(topleft = spiller2.x).center)
    
    if bil1_v2.x == bil2.v2.x:
        spiller1.kreasj()
        spiller2.kreasj()
    
 """   

#gjør sånn at man kan droppe denne
def draw2(surface, img, spiller, pos):
    
    #surface.blit(img, pos)
    
    
    
    spiller.draw(surface)
    pg.display.update()


        
        

#lager vindu

pg.init()

spiller1 = Spiller1(4, 4)
spiller2 = Spiller2(4, 4)
surface = pg.display.set_mode(SIZE)

run = True

start = True
clock = pg.time.Clock()



while run:
    clock.tick(FPS)
        
  
    while start == True:
       surface.fill(black)
       startside()
       pg.display.update()
       for event in pg.event.get():
           
           if event.type == pg.QUIT:
               run = False
               break
           if event.type == pg.KEYDOWN:
                start = False
                valg = True
           break
        

    


        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        
        
        
#sett dette inn i i en klasse
        
    
    
    #overfører filer til spill
    surface.blit(gress, (0, 0))
    surface.blit(bane, (0, 0))
    surface.blit(finish, (180, 30))
    
    
    draw2(surface, bil1, spiller1, (200, 60))
    draw2(surface, bil2, spiller2, (200, 40))
    
    #surface.blit(bil1, (140, 40 ))
    #surface.blit(bil2, (140, 75))
    
    bevegelse_av_bil1(spiller1)
    bevegelse_av_bil2(spiller2)
    
    #tegnTekst(f"tid:{tid()}", 100, 550, black, 15)
    
    #runde_text = font2.render(f"Runde: {Info.runde}", 1, black)
    #surface.blit(runde_text, (50, 550))
    
    #tid_text = font2.render(f"tid: {Info.get_level_time()}", 1, black)
    #surface.blit(tid_text, (50, 560))
    

    
    

    
    if spiller1.kollisjon(bane_outline_mask) != None:
        spiller1.kreasj()
        
    if spiller2.kollisjon(bane_outline_mask) != None:
        spiller2.kreasj()
        

    if spiller1.kollisjon(finish_mask, *finish_posisjon) != None:
        print("finish")
        
    kollisjon_med_mållinja(spiller1, spiller2)
    #kollisjon_mellom_biler(spiller1, spiller2, bil1, bil2)
    #runder(3, spiller1, spiller2)
        
    fart_text = font2.render(f"fart spiller 1: {round(spiller1.vel)} px/s", 1, black)
    surface.blit(fart_text, (50, 550))
    
    fart_text = font2.render(f"fart spiller 2: {round(spiller2.vel)} px/s", 1, black)
    surface.blit(fart_text, (450, 550))
    
    #runde_text = font2.render(f"Runde spiller1: {runde_spiller1}", 1, black)
    #surface.blit(runde_text, (50, 565))
    
    #runde_text = font2.render(f"Runde spiller2: {runde_spiller2}", 1, black)
    #surface.blit(runde_text, (450, 565))
    
    pg.display.flip()
    
 
    
pg.quit()


