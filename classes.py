import pygame

from funciones import load_spritesheets, get_block

class Player(pygame.sprite.Sprite):
    gravedad = 1
    sprites = None
    delay = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direccion = "left"
        self.ani_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        if self.sprites is None:
            self.sprites = load_spritesheets("sprites", 32, 32, True )

    def saltar(self):
        self.y_vel = -self.gravedad * 8
        self.ani_count = 0
        self.jump_count +=1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def daño(self):
        self.hit = True

    def izquierda(self, vel):
        self.x_vel = -vel
        if self.direccion != "left":
            self.direccion = "left"
            self.ani_count = 0

    def derecha(self, vel):
        self.x_vel = vel
        if self.direccion != "right":
            self.direccion = "right"
            self.ani_count = 0

    def caida(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        spritesheet = "idle"
        if self.hit == True:
            spritesheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                spritesheet = "jump"
            elif self.jump_count == 2:
                spritesheet = "double_jump"
        elif self.y_vel > self.gravedad * 2:
            spritesheet = "fall"
        elif self.x_vel != 0:
            spritesheet = "run"

        spritesheet_name = spritesheet + "_" + self.direccion
        sprites = self.sprites[spritesheet_name]
        sprite_index = (self.ani_count // self.delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.ani_count += 1
        self.actualizar()

    def actualizar(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.gravedad)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > 120:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Bloque(Objeto):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        bloque = get_block(size)
        self.image.blit(bloque, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fuego(Objeto):
    delay = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_spritesheets("Traps\Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.ani_count = 0
        self.ani_name = "off"

    def on(self):
        self.ani_name = "on"
    def off(self):
        self.ani_name = "off"

    def loop(self):
        sprites = self.fire[self.ani_name]
        sprite_index = (self.ani_count // self.delay) % len(sprites)
        self.image = sprites[sprite_index]
        self.ani_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if (self.ani_count // self.delay) > len(sprites):
            self.ani_count = 0
