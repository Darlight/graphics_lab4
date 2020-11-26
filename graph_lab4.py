"""
Universidad del Valle de Guatemala
Curso de Graficas por computadora
Lic. Dennis Aldana 
Lab4
Mario Perdomo
Carnet 18029

"""
import pygame
from math import pi, cos, sin, atan2

import pygame

colors = {
    "1":(255,0,0),
    "2":(0,255,0),
    "3":(0,0,255)
}

wall1 = pygame.image.load('./sprites/wall1.png')
wall2 = pygame.image.load('./sprites/wall2.png')
wall3 = pygame.image.load('./sprites/wall3.png')
goal = pygame.image.load('./sprites/goal_3.png')
#wall4 = pygame.image.load('./sprites/wall4.png')
#wall5 = pygame.image.load('./sprites/wall5.png')


enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": pygame.image.load('./sprites/sprite4.png')
  },
  {
    "x": 280,
    "y": 190,
    "texture": pygame.image.load('./sprites/sprite3.png')
  },
  {
    "x": 225,
    "y": 340,
    "texture": pygame.image.load('./sprites/sprite4.png')
  },
  {
    "x": 220,
    "y": 425,
    "texture": pygame.image.load('./sprites/sprite3.png')
  },
  {
    "x": 320,
    "y": 420,
    "texture": pygame.image.load('./sprites/sprite4.png')
  },
  {
    "x": 800,
    "y": 600,
    "texture": pygame.image.load('./sprites/goal_3.png')
  }
]

textures = {
    "1": wall1,
    "2": wall2,
    "3": wall3,
    "4": goal
}

hud = pygame.image.load('./sprites/hud.png')
hand = pygame.image.load('./sprites/player.png')
white = (255,255,255)
black = (0,0,0)
random_color = (0,155,255)
face = pygame.image.load('./sprites/face.png')
#el size cuadrado de los sprites de wolfenstein divido entre los blocksize
aspect_ratio = 128/50

class Raycaster:
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.map = []

        self.player = {
            "x": self.blocksize + 25,
            "y": self.blocksize + 25,
            "a": 0,
            "fov": pi/3
        }
        self.zbuffer = [-float('inf') for z in range(0, 500)]

    def point(self, x, y, c):
        screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + self.blocksize):
            for cy in range(y, y + self.blocksize):
                tx = int((cx - x) * aspect_ratio) 
                ty = int((cy - y) * aspect_ratio)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c) 

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    
    def cast_ray(self, a):
        d = 0
        while True:
            x = self.player["x"] + d * cos(a)
            y = self.player["y"] + d * sin(a)

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1< hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit* aspect_ratio)

                return d, self.map[j][i], tx

            self.point(int(x),int(y), white)
            d += 1

    def draw_stake(self, x, h, texture, tx):
        start = int(250 - h/2)
        end = int(250 + h/2)
        for y in range(start, end):
            ty = int(((y - start)*128)/(end - start))
            c = texture.get_at((tx, ty))
            self.point(x, y, c)
    
    def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = (500/sprite_d) * 70

        sprite_x = 500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x-500] >= sprite_d:
                    tx = int((x-sprite_x) * 128/sprite_size)
                    ty = int((y-sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx,ty))
                    #esto sirve para no colorear lo morado de las imagenes
                    #explicado en clase
                    if c!= (152,0,136,255):
                        self.point(x,y,c)
                        self.zbuffer[x - 500] = sprite_d

    def draw_Hud(self,xi,yi, w = 500, h = 100):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 600/w)
                ty = int((y - yi) * 90/h)
                c = hud.get_at((tx, ty))
                if c != (255,0,255):
                    #No se elimino por completo 
                    self.point(x,y,c)
    
    def draw_Face(self,xi,yi, w = 64, h = 84):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 104/w)
                ty = int((y - yi) * 114/h)
                c = face.get_at((tx, ty))
                if c != (255,0,255):
                    #No se elimino por completo 
                    self.point(x,y,c)

    def draw_player(self, xi, yi, w = 256, h = 256):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 32/w)
                ty = int((y - yi) * 32/h)
                c = hand.get_at((tx, ty))
                #esto sirve para no colorear lo morado de las imagenes
                #explicado en clase
                if c != (152, 0, 136, 255):
                    self.point(x, y, c)

    def render(self):
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ' :
                    self.draw_rectangle(x, y, textures[self.map[j][i]])

        self.point(self.player["x"], self.player["y"], white)

        for i in range(0,500):
            a = self.player["a"] - self.player["fov"]/2 + i * self.player["fov"]/500
            d, c, tx = self.cast_ray(a)

            x = 500 + i
            h = 500/(d* cos(a- self.player["a"])) * 100
            self.draw_stake(x, h, textures[c], tx)
            self.zbuffer[i] = d
        
        for enemy in enemies:
            self.point(enemy["x"], enemy["y"],black)
            self.draw_sprite(enemy)
        
        self.draw_player(1000 - 256 - 128, 500 - 256)
        self.draw_Hud(510,0)
        self.draw_Face(737,7)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def main_menu():
    #Sacado de https://pythonprogramming.net/pygame-start-menu-tutorial/
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(random_color)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Please press enter to kill Nazis!", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def win_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(random_color)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Thanks again for your time!", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
raymap = Raycaster(screen)
raymap.load_map('map.txt')


main_menu()
# Loop para que continue el juego
while True:
    #cantidad de pixeles por movimiento
    d = 10
    screen.fill(black)
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                raymap.player["a"] -= pi/20
            if e.key == pygame.K_RIGHT:
                raymap.player["a"] += pi/20

            if e.key == pygame.K_UP:
                raymap.player["x"] += int(d * cos(raymap.player["a"]))
                raymap.player["y"] += int(d * sin(raymap.player["a"]))
            if e.key == pygame.K_DOWN:
                raymap.player["x"] -= int(d * cos(raymap.player["a"]))
                raymap.player["y"] -= int(d * sin(raymap.player["a"]))
    #evento cuando se acerca al trofeo
    if(785<raymap.player["x"]<825 and 585<raymap.player["y"]<625):
        break
                
    
    raymap.render()
    pygame.display.flip()

win_screen()