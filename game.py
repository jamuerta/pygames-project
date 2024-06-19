import pygame
from os.path import join
from classes import *
from funciones import background, health_bar, game_over

pygame.init()

WIDTH, HEIGHT = 800, 600
vel = 5

ventana = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(win, fondo, fondo_i, player, objetos, offset_x):
    for tile in fondo:
        ventana.blit(fondo_i, tile)

    for obj in objetos:
        obj.draw(win, offset_x)
    
    player.draw(win, offset_x)
    pygame.display.update()

def colision_ver(player, objetos, dy):
    obj_chocados = []
    for obj in objetos:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.caida()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            obj_chocados.append(obj)
    return obj_chocados

def colision(player, objetos, dx):
    player.move(dx, 0)
    player.actualizar()
    obj_chocado = None
    for obj in objetos:
        if pygame.sprite.collide_mask(player, obj):
            obj_chocado = obj
            break

    player.move(-dx, 0)
    player.actualizar()
    return obj_chocado

def mover(player, objetos):
    teclas = pygame.key.get_pressed()

    player.x_vel = 0
    colision_izq = colision(player, objetos, -vel * 2)
    colision_der = colision(player, objetos, vel * 2)

    if teclas[pygame.K_LEFT] and not colision_izq:
        player.izquierda(vel)
    if teclas[pygame.K_RIGHT] and not colision_der:
        player.derecha(vel)

    vertical_collide = colision_ver(player, objetos, player.y_vel)
    to_check = [colision_izq, colision_der, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.daño(5)

def main(ventana):
    clock = pygame.time.Clock()
    fondo, fondo_im = background("Gray.png")

    block_size = 96

    jugador = Player(100, 100, 50, 50)
    jugador.max_health = 100
    fire = Fuego(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Bloque(i * block_size, HEIGHT - block_size, block_size, 272,64)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objetos = [*floor, Bloque(0, HEIGHT - block_size * 2, block_size, 272, 64),
               Bloque(block_size * 3, HEIGHT - block_size * 4, block_size, 272, 64), 
               Bloque(block_size * 4, HEIGHT - block_size * 4, block_size, 272, 64), 
               Bloque(block_size * 8, HEIGHT - block_size * 3, block_size, 272, 64),
               Bloque(block_size * 9, HEIGHT - block_size * 3, block_size, 272, 64),
               Bloque(block_size * 10, HEIGHT - block_size * 3, block_size, 272, 64), fire]

    offset_x = 0
    scroll_areaw = 200

    run = True
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and jugador.jump_count < 2:
                    jugador.saltar()

                if event.key == pygame.K_r and jugador.dead:
                    main(ventana)

                if event.key == pygame.K_q and jugador.dead:
                    run = False
    
        if not jugador.dead:
            jugador.loop(60)
            fire.loop()
            mover(jugador, objetos)
            draw(ventana, fondo, fondo_im, jugador, objetos, offset_x)

            if ((jugador.rect.right - offset_x >= WIDTH - scroll_areaw) and jugador.x_vel > 0) or (
                (jugador.rect.left - offset_x <= scroll_areaw) and jugador.x_vel < 0):
                offset_x += jugador.x_vel
            
            health_bar(ventana, jugador.health, jugador.max_health, 10, 10)  # Ajustar la posición según sea necesario
        else: 
            game_over(ventana, "Game Over - Press R to Restart or Q to Quit", WIDTH // 2 - 250, HEIGHT // 2 - 50)
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(ventana)
# PARA EL ÚLTIMO CONTROL : JUEGO FUNCIONAL, PPT QUE EXPLIQUE EL JUEGO (NO EL CÓDIGO)
# implementar: las plataformas, el salto
