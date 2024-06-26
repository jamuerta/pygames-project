import pygame
from classes import *
from funciones import health_bar, game_over

pygame.init()
pygame.display.set_caption("pixel quest")

WIDTH, HEIGHT = 800, 600
vel = 5
block_size = 96

ventana = pygame.display.set_mode((WIDTH, HEIGHT))

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

    if player.rect.left + player.x_vel < 0:
        player.rect.left = 0

    vertical_collide = colision_ver(player, objetos, player.y_vel)
    to_check = [colision_izq, colision_der, *vertical_collide]
    for obj in to_check:
        if isinstance(obj, Fruits):
            obj.apply_effect(player)
            obj.collect()
        if obj and obj.name == "fire":
            player.daño(5)
        elif obj and obj.name == "spikes":
            player.daño(5)
        elif obj and obj.name == "spiked ball":
            player.daño(5)

def main(ventana):
    clock = pygame.time.Clock()

    jugador = Player(100, 100, 50, 50)
    jugador.max_health = 100
    jugador.health = jugador.max_health
    

    level1 = Level(jugador, "Gray.png")
    level2 = Level(jugador, "Yellow.png")
    level3 = Level(jugador, "Blue.png")
    level4 = Level(jugador, "Brown.png")
    level5 = Level(jugador, "Purple.png")

    current_level = level1

    level1.load_game_data(objetos_nivel1)
    level2.load_game_data(objetos_nivel2)
    level3.load_game_data(objetos_nivel3)
    level4.load_game_data(objetos_nivel4)
    level5.load_game_data(objetos_nivel5)

    offset_x = 0
    scroll_areaw = 200

    run = True
    while run:
        clock.tick(60)
        #print(jugador.rect.x, jugador.rect.y)
        
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
            if jugador.rect.y <= 0:
                jugador.rect.y = 0

            if jugador.rect.right >= 2000:
                if current_level == level1:
                    current_level = level2
                elif current_level == level2:
                    current_level = level3
                elif current_level == level3:
                    current_level = level4
                elif current_level == level4:
                    current_level = level5
                elif current_level == level5:
                    game_over(ventana, "Completaste el juego! Felicidades!", WIDTH // 3, HEIGHT // 2)
                    pygame.display.update()
                    pygame.time.delay(3000)
                    pygame.quit()

                jugador.rect.left = 0  
                jugador.rect.y = 100
                offset_x = 0

            jugador.loop(60)
            n1_fire1.loop()
            n1_fire2.loop()
            n1_fire3.loop()
            n1_fruit1.loop()
            n2_fire1.loop()
            n2_fire2.loop()
            n2_fire3.loop()
            n2_fire4.loop()
            n2_fire5.loop()
            n3_fire1.loop()
            n3_fire2.loop()
            n4_fire1.loop()
            n4_fire2.loop()
            n4_fire3.loop()
            n5_fire1.loop()
            n5_fire2.loop()
            n5_fire3.loop()
            n5_fruit1.loop()
            mover(jugador, current_level.objetos)  
            current_level.upd() 
            current_level.draw(ventana, offset_x)  
            jugador.draw(ventana, offset_x)

            if ((jugador.rect.right - offset_x >= WIDTH - scroll_areaw) and jugador.x_vel > 0) or (
                (jugador.rect.left - offset_x <= 0) and jugador.x_vel < 0):
                offset_x += jugador.x_vel
            
            health_bar(ventana, jugador.health, jugador.max_health, 10, 10)  # Ajustar la posición según sea necesario
        else: 
            game_over(ventana, "Game Over - R para Reiniciar, Q para Salir", WIDTH // 2 - 250, HEIGHT // 2 - 50)
        
        pygame.display.flip()

    pygame.quit()
    quit()

##############################################################

n1_fire1 = Fuego(1000, 250, 16, 32)
n1_fire2 = Fuego(100, HEIGHT - block_size - 64, 16, 32)
n1_fire3 = Fuego(355, 152, 16, 32)

n1_fruit1 = health_fruit(770, 250, 32, 32, "Cherries")

floor_1 = [Bloque(i * block_size, HEIGHT - block_size, block_size, 272,64)
             for i in range(0, 2000)]
objetos_nivel1 = [*floor_1, Bloque(0, HEIGHT - block_size * 2, block_size, 272, 64),
               Bloque(block_size * 3, HEIGHT - block_size * 4, block_size, 272, 64), 
               Bloque(block_size * 4, HEIGHT - block_size * 4, block_size, 272, 64), 
               Bloque(block_size * 8, HEIGHT - block_size * 3, block_size, 272, 64),
               Bloque(block_size * 9, HEIGHT - block_size * 3, block_size, 272, 64),
               Bloque(block_size * 10, HEIGHT - block_size * 3, block_size, 272, 64),
               Bloque(block_size * 13, HEIGHT - block_size * 4, block_size, 272, 64),
                Bloque(block_size * 14, HEIGHT - block_size * 5, block_size, 272, 64),
                Bloque(block_size * 15, HEIGHT - block_size * 5, block_size, 272, 64),
                Bloque(block_size * 16, HEIGHT - block_size * 5, block_size, 272, 64),
                Bloque(block_size * 18, HEIGHT - block_size * 2, block_size, 272, 64),
                Bloque(block_size * 19, HEIGHT - block_size * 2, block_size, 272, 64),
                 Spikes(1100, 475, 28, 28), Spikes(1120, 475, 28, 28), Spikes(1140, 475, 28, 28),
                 Spikes(1410, 92, 28, 28), Spikes(1505, 92, 28, 28),
                 Spiked_Ball(595, 440, 40, 40), Spiked_Ball(1300, 152, 40, 40), Spiked_Ball(1415, 300, 40, 40),
                 Spiked_Ball(1770, 344, 40, 40),
                 n1_fruit1, n1_fire2, n1_fire1, n1_fire3]

################################################################

floor_2 = [Bloque(i * block_size, HEIGHT - block_size, block_size, 96, 128)
           for i in range(0, 2000)]
n2_fire1 = Fuego(130, 440, 16, 32)
n2_fire2 = Fuego(500, 250, 16, 32)
n2_fire3 = Fuego(640, 440, 16, 32)
n2_fire4 = Fuego(1715, 440, 16, 32)
n2_fire5 = Fuego(1950, 440, 16, 32)


objetos_nivel2 = [*floor_2, 
                  Bloque(block_size * 2, HEIGHT - block_size * 2, block_size, 96, 128),
                  Bloque(block_size * 5, HEIGHT - block_size * 3, block_size, 96, 128), 
                  Bloque(block_size * 4, HEIGHT - block_size * 4, block_size, 96, 128), 
                  Bloque(block_size * 8, HEIGHT - block_size * 3, block_size, 96, 128),
                  Bloque(block_size * 9, HEIGHT - block_size * 3, block_size, 96, 128),
                  Bloque(block_size * 10, HEIGHT - block_size * 3, block_size, 96, 128),
                  Bloque(block_size * 13, HEIGHT - block_size * 4, block_size, 96, 128),
                  Bloque(block_size * 14, HEIGHT - block_size * 5, block_size, 96, 128),
                  Bloque(block_size * 16, HEIGHT - block_size * 5, block_size, 96, 128),
                  Bloque(block_size * 18, HEIGHT - block_size * 3, block_size, 96, 128),
                  Spikes(870, 285, 28, 28), Spikes(900, 285, 28, 28),
                  Spikes(930, 285, 28, 28), Spikes(960, 285, 28, 28), Spikes(1460, 475, 28, 28),
                  Spikes(1490, 475, 28, 28),
                  Spikes(1520, 475, 28, 28), Spiked_Ball(1760, 260, 40, 40),
                  n2_fire1, n2_fire2, n2_fire3, n2_fire4, n2_fire5]

################################################################

n3_fire1 = Fuego(150, HEIGHT - block_size - 64, 16, 32)
n3_fire2 = Fuego(1710, 440, 16, 32)


floor_3 = [Bloque(i * block_size, HEIGHT - block_size, block_size, 0, 0)
           for i in range(0, 2000)]
objetos_nivel3 = [*floor_3, 
                  Bloque(block_size * 3, HEIGHT - block_size * 2, block_size, 0, 0),
                  Bloque(block_size * 3, HEIGHT - block_size * 3, block_size, 0, 0), 
                  Bloque(block_size * 3, HEIGHT - block_size * 5, block_size, 0, 0), 
                  Bloque(block_size * 3, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 3, HEIGHT - block_size * 7, block_size, 0, 0),
                  Bloque(block_size * 6, HEIGHT - block_size * 3, block_size, 0, 0),
                  Bloque(block_size * 6, HEIGHT - block_size * 4, block_size, 0, 0),
                  Bloque(block_size * 6, HEIGHT - block_size * 5, block_size, 0, 0),
                  Bloque(block_size * 6, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 6, HEIGHT - block_size * 7, block_size, 0, 0),
                  Bloque(block_size * 10, HEIGHT - block_size * 2, block_size, 0, 0),
                  Bloque(block_size * 10, HEIGHT - block_size * 4, block_size, 0, 0), 
                  Bloque(block_size * 10, HEIGHT - block_size * 5, block_size, 0, 0), 
                  Bloque(block_size * 10, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 10, HEIGHT - block_size * 7, block_size, 0, 0),
                  Bloque(block_size * 12, HEIGHT - block_size * 3, block_size, 0, 0),
                  Bloque(block_size * 12, HEIGHT - block_size * 4, block_size, 0, 0), 
                  Bloque(block_size * 12, HEIGHT - block_size * 5, block_size, 0, 0), 
                  Bloque(block_size * 12, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 12, HEIGHT - block_size * 7, block_size, 0, 0),
                  Bloque(block_size * 16, HEIGHT - block_size * 2, block_size, 0, 0),
                  Bloque(block_size * 16, HEIGHT - block_size * 3, block_size, 0, 0), 
                  Bloque(block_size * 16, HEIGHT - block_size * 5, block_size, 0, 0), 
                  Bloque(block_size * 16, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 16, HEIGHT - block_size * 7, block_size, 0, 0),
                  Bloque(block_size * 19, HEIGHT - block_size * 2, block_size, 0, 0),
                  Bloque(block_size * 19, HEIGHT - block_size * 4, block_size, 0, 0),
                  Bloque(block_size * 19, HEIGHT - block_size * 5, block_size, 0, 0),
                  Bloque(block_size * 19, HEIGHT - block_size * 6, block_size, 0, 0),
                  Bloque(block_size * 19, HEIGHT - block_size * 7, block_size, 0, 0),
                  Spikes(430, 475, 28, 28), Spikes(460, 475, 28, 28), Spikes(490, 475, 28, 28),
                  Spikes(1320, 475, 28, 28), Spikes(1350, 475, 28, 28), Spiked_Ball(830, 330, 40, 40),
                  Spiked_Ball(1400, 230, 40, 40),
                  n3_fire1, n3_fire2]

################################################################

n4_fire1 = Fuego(370, HEIGHT - block_size - 64, 16, 32)
n4_fire2 = Fuego(1465, 248, 16, 32)
n4_fire3 = Fuego(1885, HEIGHT -block_size - 64, 16, 32)


floor_4 = [Bloque(i * block_size, HEIGHT - block_size, block_size, 96, 64)
           for i in range(0, 2000)]

objetos_nivel4 = [*floor_4,
                   Bloque(block_size, HEIGHT - block_size * 2, block_size, 96, 64), 
                  Bloque(block_size * 3, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 4, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 7, HEIGHT - block_size * 2, block_size, 96, 64),
                  Bloque(block_size * 8, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 9, HEIGHT - block_size * 4, block_size, 96, 64),
                  Bloque(block_size * 10, HEIGHT - block_size * 5, block_size, 96, 64),
                  Bloque(block_size * 11, HEIGHT - block_size * 5, block_size, 96, 64),
                  Bloque(block_size * 12, HEIGHT - block_size * 5, block_size, 96, 64),
                  Bloque(block_size * 15, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 16, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 17, HEIGHT - block_size * 3, block_size, 96, 64),
                  Bloque(block_size * 18, HEIGHT - block_size * 4, block_size, 96, 64),
                  Spikes(1250, 475, 28, 28), Spikes(1280, 475, 28, 28), Spikes(1310, 475, 28, 28),
                  Spikes(770, 285, 28, 28), Spikes(1040, 92, 28, 28), Spikes(1130, 92, 28, 28),
                  Spikes(1700, 476, 28, 28), Spiked_Ball(360, 200, 40, 40), Spiked_Ball(1740, 50, 40, 40),
                  n4_fire1, n4_fire2, n4_fire3]

##############################################################

n5_fire1 = Fuego(250, 344, 16, 32)
n5_fire2 = Fuego(1310, 248, 16, 32)
n5_fire3 = Fuego(1935, 440, 16, 32)


n5_fruit1 = speed_fruit(450, 152, 32, 32, "Bananas")



floor_5 = [Bloque(i * block_size, HEIGHT - block_size, block_size, 0, 64)
           for i in range(0, 2000)]

objetos_nivel5 = [*floor_5, n5_fire3, n5_fruit1,
                  Bloque(block_size, HEIGHT - block_size * 2, block_size, 0, 64),
                  Bloque(block_size * 2, HEIGHT - block_size * 2, block_size, 0, 64), 
                  Bloque(block_size * 4, HEIGHT - block_size * 4, block_size, 0, 64), 
                  Bloque(block_size * 5, HEIGHT - block_size * 4, block_size, 0, 64),
                  Bloque(block_size * 9, HEIGHT - block_size * 5, block_size, 0, 64),
                  Bloque(block_size * 10, HEIGHT - block_size * 5, block_size, 0, 64),
                  Bloque(block_size * 13, HEIGHT - block_size * 3, block_size, 0, 64),
                  Bloque(block_size * 14, HEIGHT - block_size * 3, block_size, 0, 64),
                  Bloque(block_size * 17, HEIGHT - block_size * 2, block_size, 0, 64),
                  Bloque(block_size * 18, HEIGHT - block_size * 2, block_size, 0, 64),
                  Bloque(block_size * 18, HEIGHT - block_size * 3, block_size, 0, 64),
                  Spikes(630, 476, 28, 28), Spikes(660, 476, 28, 28), Spikes(310, 476, 28, 28),
                  Spikes(900, 92, 28, 28), Spikes(930, 92, 28, 28), Spikes(1140, 476, 28, 28),
                  Spikes(1110, 476, 28, 28), Spikes(6700, 380, 28, 28), Spiked_Ball(650, 150, 40, 40),
                  Spiked_Ball(840, 320, 40, 40), Spiked_Ball(1500, 250, 40, 40),
                  n5_fire1, n5_fire2]

if __name__ == "__main__":
    main(ventana)
# PARA EL ÚLTIMO CONTROL : JUEGO FUNCIONAL, PPT QUE EXPLIQUE EL JUEGO (NO EL CÓDIGO)
# implementar: las plataformas, el salto
