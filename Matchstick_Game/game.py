#/usr/bin/env python3

import os
import time
import pygame
from pygame.locals import *


def load_image2(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class matches():
    def __init__(self, n):
        self.sticks = n
        self.limit = 2

    def withdraw(self, nb):
        retrait = min(nb, self.limit)
        self.sticks -= retrait
        self.limit = 2*retrait
        if (self.sticks > 0):
            return True
        else:
            return False

    def fin(self):
        if (self.sticks > 0):
            return True
        else:
            return False

    def player(self):
        ret = 1
        wait = True

        while wait:
            draw_on_board(ret,"You can", "Press Up and Down arrow to modify number of matches you want to remove, Press right arrow to continue")
#        ret = eval(input("How much matches you want to take out ? ==> "))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if ret < self.limit:
                            ret += 1
                    elif event.key == pygame.K_DOWN:
                        if ret > 1:
                            ret -= 1
                    elif event.key == pygame.K_RIGHT:
                        wait = False

        return ret

    def AI(self):
        draw_on_board(1, "I can", "")
        if self.sticks == 1:
            nb = 1
            draw_on_board(1, "I can", "Nice move !")
        elif self.limit >= (self.sticks-1):
            nb = self.sticks-1
            draw_on_board(nb, "I can", "I think you're in trouble...")
        else :
            laisse = 2 * (self.limit+1)
            nb = max(1, min(self.limit, self.sticks - laisse))

        draw_on_board(nb,"I can", "My turn, I take out %i, Press right arrow to continue " % nb)

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        wait  = False

        return nb


def playagainOrexit():
    pygame.event.clear()
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            if event.key == K_q:
                return False
            else:
                return True
    return False


def creaTexteObj(texte, Police):
    texteSurface = Police.render(texte, True, white)
    return texteSurface, texteSurface.get_rect()


def gameOver(msg):
    GOTexte =  pygame.font.Font('BradBunR.ttf', 150)
    petitTexte =  pygame.font.Font('BradBunR.ttf', 20)

    GOTexteSurf, GOTexteRect = creaTexteObj(msg, GOTexte)
    petitTexteSurf, petitTexteRect = creaTexteObj("Press any button", petitTexte)

    GOTexteRect.center = surfaceW/2, ((surfaceH/2)-50)
    surface.blit(GOTexteSurf, GOTexteRect)

    petitTexteRect.center = surfaceW/2, ((surfaceH/2)+50)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()


def score(compte):
    police =  pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("Score : "+str(compte), True, white)
    surface.blit(texte,[10,0])


def dessine(x, y, image):
    surface.blit(image, (x,y))


def draw_on_board(withdraw, status, msg):
    surface.fill(background_color)

    x0 = 35
    xstep = 40
    xmax = x0 + 30 * xstep
    compteur = 0
    y0 = 210
    ymax = 260

    y = y0
    for x in range(x0, xmax, xstep):
        compteur += 1
        dessine(x, y, img)
        if compteur >= matchstick.sticks:
            x = xmax
            y = ymax

    compteurwithdraw =  pygame.font.Font('BradBunR.ttf', 150)
    withdrawSurf, withdrawRect = creaTexteObj(str(withdraw), compteurwithdraw)
    withdrawRect.center = 1365/2, 650/5
    surface.blit(withdrawSurf, withdrawRect)

    police =  pygame.font.Font('BradBunR.ttf', 28)
    texte = police.render("%s take out from 1 to %i" % (status, min(matchstick.limit, matchstick.sticks)), True, white)
    surface.blit(texte, [10, 0])

    WIDTH = HEIGHT = 500
    police = pygame.font.Font('BradBunR.ttf', 28)
    text = police.render("%s" % (msg), True, white)
    text_rect = text.get_rect(center=(surfaceW/2, surfaceH/2))
    surface.blit(text, [10, 30])


    pygame.display.update()

# Init
pygame.init()
pygame.mixer.init()

surfaceW = 1365
surfaceH = 650
white = (0,0,0)
background_color = (245, 245, 245)

s = 'sound'
music = pygame.mixer.music.load(os.path.join(s, 'music.ogg'))
pygame.mixer.music.play(-1)

img = pygame.image.load('test.png')

surface = pygame.display.set_mode((surfaceW,surfaceH))
pygame.display.set_caption("Matchstick")


def main():
    global matchstick

    matchstick = matches(30)

    while matchstick.fin():

        withdraw = matchstick.player()
        takeout = matchstick.withdraw(withdraw)

        pygame.event.clear()
        event = pygame.event.wait()

        if takeout:
            withdraw = matchstick.AI()
            takeout = matchstick.withdraw(withdraw)
            if not takeout:
                gameOver("Bravo ! You Win !")
        else:
            gameOver("Booh ! You lost !")
        pygame.display.update()


playagain = True
while playagain:
    main()
    time.sleep(2)
    playagain = playagainOrexit()

pygame.quit()
quit()