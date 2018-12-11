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
background = pygame.image.load("background.jpg").convert()
paremale_suunatud = pygame.image.load("paremale.png").convert_alpha()
vasakule_suunatud = pygame.image.load("vasakule.png").convert_alpha()
herilane = pygame.image.load("herilane.png").convert_alpha()
kärbes = pygame.image.load("kärbes.png").convert_alpha()
konserv = pygame.image.load("konserv.png").convert_alpha()

#taustamuusika
pygame.mixer.music.load("muusika.mp3")
pygame.mixer.music.play(-1,0.0)

#vajaminevad muutujad
font = pygame.font.SysFont("Arial",35)
font2 = pygame.font.SysFont("Century Gothic",35)
skoori_fail = "skoorid.txt"
tekst = "lõpp"
kiirus = 5
skoor = 0
energiariba_laius = 1000
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
konserv_väärtus = False
konserv_ekraanil = False
asukoha_muutus = True
liigub = True
game_over = False
mängu_algus = True
vasakule = False
paremale = True
asukoha_muutus = True

#vajaminevad funktsioonid
def draw_text(tekst, x_positsioon, y_positsioon):
    #suvalise teksti kuvamiseks
    #http://kidscancode.org/blog/2016/11/pygame_shmup_part_14/
    tekst1 = tekst
    tekst_ekraanile = font2.render(tekst1, True, (20,20,20))
    return mänguaken.blit(tekst_ekraanile, [x_positsioon,y_positsioon])

def algusaken():
    #http://kidscancode.org/blog/2016/11/pygame_shmup_part_14/
    global liigub
    mänguaken.blit(background, (0,0))
    draw_text("Liigu nuppude abil ning püüa kärbseid",
              265, 200)
    draw_text("Mäng on läbi, kui energia saab otsa või kui lähed vastu herilast",
              65, 300) 
    draw_text(" Konservi püüdes saad energiat juurde",
              265, 400)
    draw_text("Alustamiseks vajuta 'Enter'", 395, 600)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.mixer.music.pause()
            if event.type == pygame.QUIT:
                liigub = False
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
              
def lõppaken(tekst):
    #http://kidscancode.org/blog/2016/11/pygame_shmup_part_14/
    global liigub
    mänguaken.blit(background, (0,0))
    draw_text(tekst, 425, 50)
    draw_text("SINU SKOOR: " + str(skoor), 100, 180)
    draw_text("5 PARIMAT", 800, 180)
    draw_text("Uuesti mängimiseks vajuta 'Enter'", 320, 650)
    
    kõik_skoorid, mängija_koht = edetabel("skoorid.txt", skoor)
    draw_text("SINU KOHT TABELIS: "+str(mängija_koht), 100, 400)
    koht = 1
    y = 250
    if len(kõik_skoorid) < 5:
        for i in range(len(kõik_skoorid)):
            skoor_tabelisse = kõik_skoorid[i]
            draw_text(str(koht)+". "+str(skoor_tabelisse)+" punkti", 800, y)
            koht+=1
            y+=70
    else:
        for i in range(5):
            skoor_tabelisse = kõik_skoorid[i]
            if skoor_tabelisse == 1:
                draw_text(str(koht)+". "+str(skoor_tabelisse)+" punkt", 800, y)
            else:
                draw_text(str(koht)+". "+str(skoor_tabelisse)+" punkti", 800, y)
            koht+=1
            y+=70
        
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.mixer.music.pause()
            if event.type == pygame.QUIT:
                liigub = False
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def edetabel(skoori_fail, skoor):
    # https://www.dreamincode.net/forums/topic/395940-a-highscore-module-for-pygame/
    fail = open(skoori_fail)
    try:
        kõik_skoorid = fail.readlines()
    except:
        kõik_skoorid = []
    fail.close
    
    for i in range(len(kõik_skoorid)):
        kõik_skoorid[i] = int(kõik_skoorid[i].strip())
    kõik_skoorid.append(skoor)    
    kõik_skoorid.sort(reverse=True)    
    mängija_koht = (kõik_skoorid.index(skoor) +1) #sest indeksid hakkavad 0-st
    
    skoorid = []
    
    for i in range(len(kõik_skoorid)):
        skoorid.append(str(kõik_skoorid[i]) + "\n")
    fail2 = open(skoori_fail, "w")
    
    for el in skoorid:
        fail2.write(el)
    fail2.close
    
    return kõik_skoorid, mängija_koht

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
    while not x_herilane >= x_kass + 110 and x_herilane <= x_kass - 110 and y_herilane >= y_kass + 110 and y_herilane <= y_kass - 110:
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
    return mänguaken.blit(tekst_ekraanile, [1025,0])
    
def mänguaken_uuesti():
    mänguaken.blit(background, (0,0))
    skoori_näitamine()
    pygame.draw.rect(mänguaken, (176,226,255), (0,0, energiariba_laius, energiariba_kõrgus))
    mänguaken.blit(herilane, (x_herilane, y_herilane))
    mänguaken.blit(kärbes, (x_kärbes, y_kärbes))
    if konserv_ekraanil == True:
        mänguaken.blit(konserv, (x_konserv, y_konserv))
    if vasakule == True:
        mänguaken.blit(vasakule_suunatud, (x_kass , y_kass))
    elif paremale == True:
        mänguaken.blit(paremale_suunatud, (x_kass , y_kass))
    pygame.display.update()
    pygame.display.flip()

#main loop
while liigub:
    pygame.time.delay(5)
    energiariba_laius -= 0.6
        
    if mängu_algus == True:
        algusaken()
        mängu_algus = False
    if game_over == True:
        lõppaken(tekst)
        skoor = 0
        energiariba_laius = 1000
        x_kass = 100
        y_kass= 50
        asukoha_muutus = True
        game_over = False
    if energiariba_laius <= 2:
        game_over = True
        tekst = "KASS VÄSIS ÄRA..."
    #loob konservi ilmumiseks x ja y koordinaadid
    if randint(0,250) == randint(0,250) and konserv_ekraanil == False:
        koordinaadid = konservi_asukoht()
        x_konserv = koordinaadid[0]
        y_konserv = koordinaadid[1] 
        konserv_ekraanil = True
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
    #kui vajutada s nuppu, siis muusika jääb seisma
    if nupud[pygame.K_s]:
        pygame.mixer.music.pause()
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
        if x_kärbes <= x_kass + 70 and x_kärbes >= x_kass - 5 and y_kärbes <= y_kass +75 and y_kärbes >= y_kass -35:
            x_herilane = herilase_asukoht()[0]
            y_herilane = herilase_asukoht()[1]
            x_kärbes = kärbse_asukoht()[0]
            y_kärbes = kärbse_asukoht()[1]
            skoor += 1
        elif x_herilane <= x_kass + 70 and x_herilane >= x_kass - 7 and y_herilane <= y_kass +75 and y_herilane >= y_kass -35:
            #läks vastu herilast ehk mäng läbi
            game_over = True
            tekst = "AIA, HERILANE SUTSAS! :("
        if konserv_väärtus == True:
            if x_konserv <= x_kass + 70 and x_konserv >= x_kass - 7 and y_konserv <= y_kass +75 and y_konserv >= y_kass -35:
                konserv_väärtus = False
                konserv_ekraanil = False
                if 700 >= energiariba_laius:
                    energiariba_laius += 225 
                else:
                    energiariba_laius += 1000-energiariba_laius 
    elif paremale == True:
        if x_kärbes >= x_kass -15 and x_kärbes <= x_kass + 80 and y_kärbes >= y_kass -15 and y_kärbes <= y_kass + 60:
            x_herilane = herilase_asukoht()[0]
            y_herilane = herilase_asukoht()[1]
            x_kärbes = kärbse_asukoht()[0]
            y_kärbes = kärbse_asukoht()[1]
            skoor += 1
        elif x_herilane >= x_kass -15 and x_herilane <= x_kass + 80 and y_herilane >= y_kass -15 and y_herilane <= y_kass + 60:
            #läks vastu herilast ehk mäng läbi
            game_over = True
            tekst = "AIA, HERILANE SUTSAS! :("
        if konserv_väärtus == True:
            if x_konserv >= x_kass -15 and x_konserv <= x_kass + 80 and y_konserv >= y_kass -15 and y_konserv <= y_kass + 60:
                konserv_väärtus = False
                konserv_ekraanil = False
                if 700 >= energiariba_laius:
                    energiariba_laius += 225 
                else:
                    energiariba_laius += 1000-energiariba_laius 
    mänguaken_uuesti()
            
pygame.quit()