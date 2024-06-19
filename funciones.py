import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 800, 600
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
vel = 5

def background(nombre):
    imagen = pygame.image.load(join("assets", "Background", nombre))
    _, _, width_i, height_i = imagen.get_rect()
    tiles = []
    
    for i in range(800 // width_i + 1):
        for j in range(600 // height_i +1):
            pos = [i* width_i, j* height_i]
            tiles.append(pos)

    return tiles, imagen
    

def flip(sprites):
    return[pygame.transform.flip(sprite, True, False) 
           for sprite in sprites]

def load_spritesheets(dir, width, height, direccion=False):
    path = join("assets", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    allsprites = {}

    for image in images:
        spritesheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(spritesheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(spritesheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direccion:
            allsprites[image.replace(".png", "")+ "_right"] = sprites
            allsprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            allsprites[image.replace(".png", "")] = sprites

    return allsprites

def get_block(size, x, y):
    path = join("assets", "Terrain", "Terrain.png")
    imagen = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

    x_pos = x
    y_pos = y
    surface.blit(imagen, (0,0), pygame.Rect(x_pos, y_pos, size, size))
    
    return pygame.transform.scale2x(surface)

def health_bar(ventana, health, max_health, x, y):
    heart_full = pygame.image.load('assets/health bar/full.png')
    heart_half = pygame.image.load('assets/health bar/half.png')
    heart_empty = pygame.image.load('assets/health bar/empty.png')
    
    full_hearts = health // 20
    half_hearts = (health % 20) // 10
    empty_hearts = (max_health // 20) - full_hearts - half_hearts

   
    for i in range(full_hearts):
        ventana.blit(heart_full, (x + i * heart_full.get_width(), y))
    
    for i in range(half_hearts):
        ventana.blit(heart_half, (x + (full_hearts + i) * heart_full.get_width(), y))
    
    for i in range(empty_hearts):
        ventana.blit(heart_empty, (x + (full_hearts + half_hearts + i) * heart_full.get_width(), y))

def game_over(ventana, message, x, y):
    font = pygame.font.SysFont('Comic Sans MS', 20)
    text = font.render(message, True, (0,0,0))
    ventana.blit(text, (x, y))