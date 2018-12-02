##https://www.youtube.com/playlist?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5
#kasutasime mängu loomisel playlistis olevate videote abi, ehk ülesehitus on sarnane

import pygame
from random import randint
pygame.init()

akna_laius = 1200
akna_kõrgus = 750

mänguaken = pygame.display.set_mode((akna_laius, akna_kõrgus))
pygame.display.set_caption("Kassimäng")

#kõik pildid, mida mängus vaja
background = pygame.image.load("background.jpg")
paremale_suunatud = pygame.image.load("paremale.png")
vasakule_suunatud = pygame.image.load("vasakule.png")
herilane = pygame.image.load("herilane.png")
kärbes = pygame.image.load("kärbes.png")
konserv = pygame.image.load("konserv.png")

#vajaminevad muutujad
font = pygame.font.SysFont("Arial",35)
font2 = pygame.font.SysFont("Arial",35)
kiirus = 8
vasakule = False
paremale = True
asukoha_muutus = True
skoor = 0
energiariba_laius = 1025
energiariba_kõrgus = 30
x_kass = 100
y_kass= 50
kassi_laius = 145
kassi_kõrgus = 80
kärbse_laius = 35
kärbse_kõrgus = 35
herilase_laius = 35
herilase_kõrgus = 35
konservi_laius = 45
konservi_kõrgus = 30
x_konserv = randint(0,1200) 
y_konserv = randint(150,750)


#vajaminevad funktsioonid
#suvalise teksti kuvamiseks
def draw_text(tekst, x_positsioon, y_positsioon):
    tekst1 = tekst
    tekst_ekraanile = font2.render(tekst1, True, (0,0,0))
    return mänguaken.blit(tekst_ekraanile, [x_positsioon,y_positsioon])

def algusaken():
    mänguaken.blit(background, (0,0))
    draw_text("Liigu nuppude abil ning püüa kärbseid.",
              375, 200)
    draw_text("Mäng on läbi, kui energia saab otsa või kui lähed vastu herilast.",
              200, 300) 
    draw_text(" Konservi püüdes saad energiat juurde.",
              375, 400)
    draw_text("Vajuta mingit nuppu, et alustada", 410, 600)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def kärbse_asukoht():
    x_kärbes = randint(100,1100)
    y_kärbes = randint(30,650)
    while not x_kärbes >= x_kass + 110 and x_kärbes <= x_kass - 110 and y_kärbes >= y_kass + 45 and y_kärbes <= y_kass - 45 and x_kärbes >= x_herilane + 45 and x_kärbes <= x_herilane - 45 and y_kärbes >= y_herilane + 45 and y_kärbes <= y_herilane - 45:
        x_kärbes = randint(0,1200)
        y_kärbes = randint(150,650)
    return [x_kärbes, y_kärbes]

def herilase_asukoht():       
    x_herilane = randint(100,1100)
    y_herilane = randint(150,650)
    while not x_herilane >= x_kass + 110 and x_herilane <= x_kass - 110 and y_herilane >= y_kass + 45 and y_herilane <= y_kass - 45:
        x_herilane = randint(0,1200) 
        y_herilane = randint(150,650)
    return [x_herilane, y_herilane]

def konservi_asukoht():
    x_konserv = randint(100,1100) 
    y_konserv = randint(150,650)
    while not x_konserv >= x_kass + 110 and x_konserv <= x_kass - 110 and y_konserv >= y_kass + 45 and y_konserv <= y_kass - 45 and x_konserv >= x_herilane + 45 and x_konserv <= x_herilane - 45 and y_konserv >= y_herilane + 45 and y_konserv <= y_herilane - 45 and x_konserv >= x_kärbes + 110 and x_konserv <= x_kärbes - 110 and y_konserv >= y_kärbes + 45 and y_konserv <= y_kärbes - 45:
        x_konserv = randint(100,1100) 
        y_konserv = randint(150,650)
    return (x_konserv, y_konserv)

#https://www.youtube.com/watch?v=PzG-fnci8uE
def skoori_näitamine():
    skoori_tekst = "SKOOR: " + str(skoor)
    tekst_ekraanile = font.render(skoori_tekst, True, (255,182,193))
    return mänguaken.blit(tekst_ekraanile, [1050,0])
    
def mänguaken_uuesti():
    mänguaken.blit(background, (0,0))
    skoori_näitamine()
    pygame.draw.rect(mänguaken, (176,226,255), (0,0, energiariba_laius, energiariba_kõrgus))
    mänguaken.blit(herilane, (x_herilane, y_herilane))
    mänguaken.blit(kärbes, (x_kärbes, y_kärbes))
    if konserv_väärtus == True:
        mänguaken.blit(konserv, (x_konserv, y_konserv))
    if vasakule == True:
        mänguaken.blit(vasakule_suunatud, (x_kass , y_kass))
    elif paremale == True:
        mänguaken.blit(paremale_suunatud, (x_kass , y_kass))
    pygame.display.update()

     
#main loop
konserv_väärtus = False
liigub = True
game_over = False
mängu_algus = True

while liigub:
    pygame.time.delay(5)
    energiariba_laius -= 1.3
    if mängu_algus == True:
        algusaken()
        mängu_algus = False
    #if game_over == True:
        #siia peaks tegema mingi funktsiooni vms et tuleks game over ekraan
    if energiariba_laius <= 2:
        liigub = False
        #game_over = True
    if randint(0,500) == randint(0,500) and konserv_väärtus == False:
        konservi_asukoht()
        konserv_väärtus = True
    #Selleks, et alguses kärbes ja herilane kuhugi saada
    if asukoha_muutus == True:
        x_herilane = herilase_asukoht()[0]
        y_herilane = herilase_asukoht()[1]
        x_kärbes = kärbse_asukoht()[0]
        y_kärbes = kärbse_asukoht()[1]
        #asukoha muutus peab olema edaspidi False, et iga kord kui tsüklit
        #uuesti teeb, ei määrataks kärbsele ja herilasele uut asukohta
        asukoha_muutus = False
        
    for event in pygame.event.get():
        #registreerib ära, kui vajutati X nuppu ehk taheti mäng sulgeda
        if event.type == pygame.QUIT:
            liigub = False
            
    nupud = pygame.key.get_pressed()
    if nupud[pygame.K_LEFT] and x_kass > kiirus - 6:
        x_kass -= kiirus
        vasakule = True
        paremale = False
    elif nupud[pygame.K_RIGHT] and x_kass < akna_laius - kassi_laius + 25:
        x_kass += kiirus
        vasakule = False
        paremale = True
    elif nupud[pygame.K_UP] and y_kass > kiirus + 30:
        y_kass -= kiirus
    elif nupud[pygame.K_DOWN] and y_kass < akna_kõrgus - kassi_kõrgus - kiirus:
        y_kass += kiirus

    #See osa selleks, et kärbes ja herilane asukohta muudaks kui kass vastu kärbest ja et mäng lõppeks, kui kass vastu herilast      
    if vasakule == True:
        if x_kärbes <= x_kass + 70 and x_kärbes >= x_kass - 7 and y_kärbes <= y_kass +75 and y_kärbes >= y_kass -35:
            x_herilane = herilase_asukoht()[0]
            y_herilane = herilase_asukoht()[1]
            x_kärbes = kärbse_asukoht()[0]
            y_kärbes = kärbse_asukoht()[1]
            skoor += 1
        elif x_herilane <= x_kass + 70 and x_herilane >= x_kass - 7 and y_herilane <= y_kass +75 and y_herilane >= y_kass -35:
            #läks vastu herilast ehk mäng läbi
            liigub = False
            #game_over = True
        elif x_konserv <= x_kass + 70 and x_konserv >= x_kass - 7 and y_konserv <= y_kass +75 and y_konserv >= y_kass -35:
            konserv_väärtus = False
            if 1000 >= energiariba_laius:
                energiariba_laius += 10 
            else:
                energiariba_laius += 1025-energiariba_laius 
    elif paremale == True:
        if x_kärbes >= x_kass -15 and x_kärbes <= x_kass + 80 and y_kärbes >= y_kass -15 and y_kärbes <= y_kass + 60:
            x_herilane = herilase_asukoht()[0]
            y_herilane = herilase_asukoht()[1]
            x_kärbes = kärbse_asukoht()[0]
            y_kärbes = kärbse_asukoht()[1]
            skoor += 1
        elif x_herilane >= x_kass -15 and x_herilane <= x_kass + 80 and y_herilane >= y_kass -15 and y_herilane <= y_kass + 60:
            #läks vastu herilast ehk mäng läbi
            liigub = False
            #game_over = True
        elif x_konserv >= x_kass -15 and x_konserv <= x_kass + 80 and y_konserv >= y_kass -15 and y_konserv <= y_kass + 60:
            konserv_väärtus = False
            if 1000 >= energiariba_laius:
                energiariba_laius += 10 
            else:
                energiariba_laius += 1025-energiariba_laius 
    mänguaken_uuesti()
            
pygame.quit()