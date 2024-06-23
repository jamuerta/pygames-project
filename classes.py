import pygame

from funciones import load_spritesheets, get_block, background

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
        self.health = 100
        self.dead = False
        self.speed_timer = None
        if self.sprites is None:
            self.sprites = load_spritesheets("sprites", 32, 32, True )

    def saltar(self):
        self.y_vel = -self.gravedad * 7
        self.ani_count = 0
        self.jump_count +=1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def daño(self, amount):
        self.hit = True
        self.health -= amount
        if self.health <= 0:
            self.health = 0
        if self.health == 0:
            self.muerte()

    def muerte(self):
        self.dead = True

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
    def __init__(self, x, y, size, x_sheet, y_sheet):
        super().__init__(x, y, size, size)
        bloque = get_block(size, x_sheet, y_sheet)
        self.image.blit(bloque, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fuego(Objeto):
    delay = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_spritesheets("Traps\Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.ani_count = 0
        self.ani_name = "on"

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

class Spikes(Objeto):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spikes")
        self.spike = pygame.image.load("assets/Traps/Spikes/Idle.png")

        #self.spikes = self.spikes["Idle"]
        self.image.blit(self.spike, (0,0))
        #self.mask = pygame.mask.from_surface(self.image)
        self.spike = pygame.transform.scale2x(self.image)

class Spiked_Ball(Objeto):
    def __init__(self, x, y ,width, height):
        super().__init__(x, y, width, height, "spiked ball")
        self.spiked_ball = pygame.image.load("assets/Traps/Spiked Ball/Spiked Ball.png")

        self.image.blit(self.spiked_ball, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fruits(Objeto):
    delay = 3
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.fruit = load_spritesheets("Fruits", width, height)
        self.image = self.fruit[name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.ani_count = 0
        self.ani_name = name
        self.collected = False

    def loop(self):
        sprites = self.fruit[self.ani_name]
        sprite_index = (self.ani_count // self.delay) % len(sprites)
        self.image = sprites[sprite_index]
        self.ani_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if (self.ani_count // self.delay) > len(sprites):
            self.ani_count = 0
            if self.collected:
                self.kill()
        

    def apply_effect(self, player):
        pass

    def collect(self):
        self.ani_name = "Collected"
        self.ani_count = 0
        self.collected = True

class speed_fruit(Fruits):
    def apply_effect(self, player):
        player.x_vel *= 2
        player.speed_timer = pygame.time.get_ticks()

    def reset_effect(self, player):
        if pygame.time.get_ticks() - player.speed_timer > 5000:
            player.x_vel /= 2
            player.speed_timer = None

class health_fruit(Fruits):
    def apply_effect(self, player):
        player.health = min(player.max_health, player.health + 20)


class Level():
    def __init__(self, player, bg_im):
        self.player = player
        self.objetos = pygame.sprite.Group()
        self.frutas = pygame.sprite.Group()
        self.fondo, self.fondo_im = background(bg_im)

    def draw(self, win, offset_x):
        for tile in self.fondo:
            win.blit(self.fondo_im, tile)

        for obj in self.objetos:
            obj.draw(win, offset_x)
    
        self.player.draw(win, offset_x)
        pygame.display.update()

    def upd(self):
        self.objetos.update()

    def load_game_data(self, objetos):
        for obj in objetos:
            if isinstance(obj, Objeto):
                self.objetos.add(obj)
            if isinstance(obj, Fruits):
                self.frutas.add(obj)

            