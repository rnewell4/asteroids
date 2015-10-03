"""Final Programming Project. Assignment 10 - Pygame - Asteroids.
The following program recreates the classic arcade game, Asteroids.
Students working on the project: Ryan Newell, Alexander Cohen, Jose Solis"""

import pygame as PG
import random as R
import math
import os
from ship import *
from rocks import *
from particles import *

def wrap(obj, size=0):
    if obj.center[0] > SIZE[0] + size:
        obj.center[0] = -(size)
    elif obj.center[0] < -(size):
        obj.center[0] = SIZE[0] + size
    if obj.center[1] > SIZE[1] + size:
        obj.center[1] = -(size)
    elif obj.center[1] < -(size):
        obj.center[1] = SIZE[1] + size


def main():
    """Setup pygame"""
    PG.init()
    PG.mixer.init()

    #Sounds
    shoot = PG.mixer.Sound(os.path.join('shoot.wav'))
    asteroid_die = PG.mixer.Sound(os.path.join('asteroid_die.wav'))

    s = PG.display.set_mode(SIZE)
    PG.display.set_caption("Assignment 10 - Asteroids")
    clock = PG.time.Clock()
    score = 0
    lives = LIVES
    levelnum = LEVEL

    """Lists of Objects"""
    asteroids = []
    for i in range(ASTEROIDS + levelnum):
        asteroids.append(Asteroid())
    enterprise = Ship()
    debris = [] #debris from ship
    debris2 = [] #debris from asteroids
    thrustballs = []
    bullets = []  # List of bullets
    #time since last bullet was shot
    time_since_press = 0

    GAMEOVER = False
    while not GAMEOVER:
        SCREEN = 0
        """Intro Screen"""
        while SCREEN == 0:
            s.fill(BLACK)
            font = PG.font.SysFont('Helvitica', 50, True, False)
            welcome = font.render("Welcome to ASTEROIDS", True, WHITE)
            initialize = font.render("Press Enter to Play", True, WHITE)
            s.blit(welcome, [SIZE[0]/2 - 200, SIZE[1]/2 - 50])
            s.blit(initialize, [SIZE[0]/2 - 150, SIZE[1]/2])

            for asteroid in asteroids:
                asteroid.draw(s)

            PG.display.flip()

            for event in PG.event.get():
                if event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                    SCREEN = 1
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()

        """Main Game"""
        while SCREEN == 1:
            clock.tick(FPS)
            time_since_press += clock.get_time()
            s.fill((0, 0, 0))
            font = PG.font.SysFont('Calibri', 25, True, False)
            scoreboard = font.render("SCORE: " + str(score), True, WHITE)
            numlives = font.render("LIVES: " + str(lives), True, WHITE)
            level = font.render("LEVEL: " + str(levelnum), True, WHITE)
            s.blit(scoreboard, [0, 0])
            s.blit(numlives, [0, 25])
            s.blit(level, [SIZE[0]-100, 0])
            
            #Draws all items on screen
            allItems = asteroids+bullets+thrustballs+debris+debris2
            for item in allItems:
                item.draw(s)

            #if debris is empty then the ship is still alive
            if debris == []:
                enterprise.draw(s)

            PG.display.flip()
            delta = clock.tick() / 1000.0
            enterprise.update(delta)

            for bullet in bullets:
                bullet.update(delta)
                
                #Checks if bullet has collided with any asteroids
                for asteroid in asteroids:
                    if abs(asteroid.center[0] - bullet.corners[0][0]) < 2 * \
                       ASIZE:
                        if collides(asteroid, bullet):
                            debris2.append(Debris(asteroid, ASIZE))
                            asteroid_die.play()
                            if asteroid.order > 1:
                                asteroids.append(Asteroid(
                                    asteroid.order - 1, asteroid.center))
                                asteroids.append(Asteroid(
                                    asteroid.order - 1, asteroid.center))
                            asteroids.remove(asteroid)
                            score = score + 20
                #removes bullet if it has outlived its lifetime
                if bullet.t > MAXT:
                    bullets.remove(bullet)

            for item in debris:
                item.update(delta)
                if item.t > MAXT * 6:
                    debris.remove(item)

            for item in debris2:
                item.update(delta)
                if item.t > MAXT*6:
                    debris2.remove(item)

            for tb in thrustballs:
                tb.update(delta)
                if tb.t > MAXT/2:
                    thrustballs.remove(tb)

            for asteroid in asteroids:
                asteroid.draw(s)
                asteroid.update(delta)

                #Only checks for collision if objects are near each other
                if abs(asteroid.center[0] - enterprise.center[0]) < 2 * ASIZE\
                   and not enterprise.is_Invincible():
                    if collides(asteroid, enterprise) or collides(enterprise,
                                                                  asteroid):
                        asteroid_die.play()
                        asteroids.remove(asteroid)
                        lives = lives - 1
                        debris.append(Debris(enterprise, SSIZE))
                        enterprise.center = array([SIZE[0] / 2, SIZE[1] / 2])
                        enterprise.vel = array([0, 0])
                        enterprise.angle = -math.pi / 2
                        enterprise.set_invincible()
            if lives == 0:
                SCREEN = 2
            if asteroids == []:
                levelnum += 1
                for i in range(ASTEROIDS + levelnum):
                    asteroids.append(Asteroid())
                enterprise.set_invincible

            """Checks if objects have gone off the screen and if so flips
            to other side"""
            for asteroid in asteroids:
                wrap(asteroid, ASIZE)

            wrap(enterprise, SSIZE)

            for bullet in bullets:
                wrap(bullet, ASIZE)

            """USER INPUT"""
            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_p:
                    SCREEN = 3

            keys = PG.key.get_pressed()
            if keys[PG.K_RIGHT]:
                enterprise.turn(math.pi/45)
            if keys[PG.K_LEFT]:
                enterprise.turn(-math.pi/45)
            if keys[PG.K_DOWN]:
                enterprise.accelerate(-.1)
            if keys[PG.K_UP]:
                if debris == []:
                    thrustballs.append(Thrust(enterprise))
                    thrustballs.append(Thrust(enterprise))
                    thrustballs.append(Thrust(enterprise))
                    enterprise.accelerate(.1)
            if keys[PG.K_SPACE]:
                if time_since_press > TIME_TO_PRESS and debris == []:
                    shoot.play()
                    bullets.append(Missile(enterprise))
                    time_since_press = 0

        while SCREEN == 2:
            s.fill((255, 255, 255))
            font = PG.font.SysFont('Helvitica', 50, True, False)
            final = font.render("GAME OVER", True, (0, 0, 0))
            scoreboard = font.render("YOUR SCORE: " + str(score), True, (0,
                                                                         0, 0))
            question = font.render("Play Again? Y/N", True, (0, 0, 0))
            s.blit(final, [SIZE[0]/2 - 150, SIZE[1]/2 - 50])
            s.blit(scoreboard, [SIZE[0]/2 - 175, SIZE[1]/2])
            s.blit(question, [SIZE[0]/2 - 175, SIZE[1]/2 + 50])

            PG.display.flip()

            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_y:
                    main()
                if event.type == PG.KEYDOWN and event.key == PG.K_n:
                    GAMEOVER = True
                    PG.quit()
                    exit()
        while SCREEN == 3:
            s.fill((255, 255, 255))
            font = PG.font.SysFont('Helvitica', 50, True, False)
            pause = font.render("GAME PAUSED", True, (0, 0, 0))
            command = font.render("PRESS P TO CONTINUE", True, (0, 0, 0))
            s.blit(pause, [SIZE[0]/2 - 150, SIZE[1]/2])
            s.blit(command, [SIZE[0]/2 - 225, SIZE[1]/2 + 50])

            PG.display.flip()

            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_p:
                    SCREEN = 1


main()
PG.quit()
exit()



