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
PINK = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial",35)
font2 = pygame.font.SysFont("Century Gothic",35)
skoori_fail = "skoorid.txt"
kiirus = 5
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
konserv_väärtus = False
konserv_ekraanil = False
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
              
def lõppaken():
    #http://kidscancode.org/blog/2016/11/pygame_shmup_part_14/
    global liigub
    mänguaken.blit(background, (0,0))
    draw_text("LÕPPSKOOR: " + str(skoor),
              465, 100)
    draw_text("Top 10 nägemiseks vajuta 'Enter'", 320, 600)
    
    nimi = enterbox(mänguaken, "Sinu nimi: ")
    if type(nimi) != bool:
        kirjuta_faili("skoorid.txt", nimi, skoor)
    
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
                skooriaken()
                
def kirjuta_faili(fail, nimi, skoor):
    f = open(fail, "a")
    f.write("\n"+str(skoor)+", "+ nimi)
    f.close
                
def enterbox(mänguaken, txt):
    # https://www.dreamincode.net/forums/topic/395940-a-highscore-module-for-pygame/
    def blink(mänguaken):
        for color in [PINK, WHITE]:
            pygame.draw.circle(box, color, (600, 220), 7, 0)
            mänguaken.blit(box, (0, by//2))
            pygame.display.flip()
            pygame.time.wait(300)

    def show_name(mänguaken, name):
        pygame.draw.rect(box, WHITE, (200, 200, bx-400, 50), 0)
        txt_surf = font.render(name, True, BLACK)
        txt_rect = txt_surf.get_rect(center=(600, 220))
        box.blit(txt_surf, txt_rect)
        mänguaken.blit(box, (0, by//2))
        pygame.display.flip()
        
    bx = 1200
    by = 300

    # tekitab kasti
    box = pygame.surface.Surface((bx, by))
    box.blit(background, (0,0))
    txt_surf = font2.render(txt, True, BLACK)
    txt_rect = txt_surf.get_rect(center=(bx//2, int(by*0.3)))
    box.blit(txt_surf, txt_rect)

    name = ""
    show_name(mänguaken, name)

    # sisestuse loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                liigub = False
                return False
            elif event.type == pygame.KEYDOWN:
                inkey = event.key
                if inkey in [13, 271]:  # enter
                    skooriaken()
                    return name
                elif inkey == 8:  # tagasi nupp
                    name = name[:-1]
                elif inkey <= 300:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= inkey >= 97:
                        inkey -= 32  # SUURED tähed
                    name += chr(inkey)

        if name == "":
            blink(mänguaken)
        show_name(mänguaken, name)

                
def skooriaken():
    global liigub
    mänguaken.blit(background, (0,0))
    skoorid = top10("skoorid.txt")
    koht = 1
    y = 125
    draw_text("TOP 10", 300, 50)
    for skoorjanimi in skoorid:
        nimi = skoorjanimi[1]
        skoor= skoorjanimi[0]
        draw_text(str(koht)+". "+nimi+"-"+str(skoor), 300, y)
        koht+=1
        y+=50
    draw_text("Edasi mängimiseks vajuta 'Enter'", 320, 650)    
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
            

def top10(skoori_fail):
    fail = open(skoori_fail, 'r')
    kõik_skoorid = fail.readlines()
    fail.close
    
    parimad10 = []
    
    for rida in kõik_skoorid:
        if len(parimad10) < 10:
            nimi_ja_skoor = rida.strip().split(", ")
            parimad10.append(nimi_ja_skoor)
    sorteeritud = list(reversed(sorted(parimad10, key = lambda x: int(x[0]))))
    return sorteeritud

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
        lõppaken()
        skoor = 0
        energiariba_laius = 1025
        asukoha_muutus = True
        game_over = False
    if energiariba_laius <= 2:
        game_over = True
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
        if konserv_väärtus == True:
            if x_konserv <= x_kass + 70 and x_konserv >= x_kass - 7 and y_konserv <= y_kass +75 and y_konserv >= y_kass -35:
                konserv_väärtus = False
                konserv_ekraanil = False
                if 1000 >= energiariba_laius:
                    energiariba_laius += 300 
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
            game_over = True
        if konserv_väärtus == True:
            if x_konserv >= x_kass -15 and x_konserv <= x_kass + 80 and y_konserv >= y_kass -15 and y_konserv <= y_kass + 60:
                konserv_väärtus = False
                konserv_ekraanil = False
                if 800 >= energiariba_laius:
                    energiariba_laius += 300 
                else:
                    energiariba_laius += 1025-energiariba_laius 
    mänguaken_uuesti()
            
pygame.quit()