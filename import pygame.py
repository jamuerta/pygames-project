import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# crear ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("nombre provisorio")

fondo = pygame.image.load("fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))


# definir la clase jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # cambiar posición inicial
        self.vel = 5
        self.vely = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if keys[pygame.K_UP]:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.rect.y += self.vel

            # PARA MANTENERLO DENTRO DE LA PANTALLA
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# crear el grupo de sprites para el jugador
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #al clickear en la x se sale del juego
            pygame.quit()
            sys.exit()

    all_sprites.update()

    screen.blit(fondo, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip() # update the contents of the entire display


    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()

# PARA EL ÚLTIMO CONTROL : JUEGO FUNCIONAL, PPT QUE EXPLIQUE EL JUEGO (NO EL CÓDIGO)
# implementar: las plataformas, el salto
