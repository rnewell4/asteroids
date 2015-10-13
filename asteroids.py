import pygame as PG
import random as R
import math
import os
from ship import *
from rocks import *
from particles import *


def wrap(obj, size=0):
    """Moves an object to opposite side of screen if it leaves the frame"""
    if obj.center[0] > SIZE[0] + size:
        obj.center[0] = -(size)
    elif obj.center[0] < -(size):
        obj.center[0] = SIZE[0] + size
    if obj.center[1] > SIZE[1] + size:
        obj.center[1] = -(size)
    elif obj.center[1] < -(size):
        obj.center[1] = SIZE[1] + size

class Game:
    """A game of asteroids"""
    def __init__(self):
        #setup pygame
        PG.init()
        PG.mixer.init()

        #Sounds
        self.shoot = PG.mixer.Sound(os.path.join('shoot.wav'))
        self.asteroid_die = PG.mixer.Sound(os.path.join('asteroid_die.wav'))

        #Setup Screen
        self.screen = PG.display.set_mode(SIZE)
        PG.display.set_caption("Assignment 10 - Asteroids")

        self.clock = PG.time.Clock()

    def setup(self):
        self.score = 0
        self.lives = LIVES
        self.levelnum = LEVEL
        self.time_since_press = 0 #time since last bullet was shot

        #Initialize objects
        self.asteroids = []
        for i in range(ASTEROIDS + self.levelnum):
            self.asteroids.append(Asteroid())
        self.enterprise = Ship()
        self.debris = [] #debris from ship
        self.debris2 = [] #debris from asteroids
        self.thrustballs = [] #ship thrust
        self.bullets = []  # List of bullets

    def run(self):
        """Run the game"""
        play = True
        while play:
            self.setup()
            self.intro_screen()
            self.play()
            play = self.game_over()
        PG.quit()

    def intro_screen(self):
        """Game waits here until players either quits or decides to play the game"""
        font = PG.font.SysFont('Helvitica', 50, True, False)
        welcome = font.render("Welcome to ASTEROIDS", True, WHITE)
        initialize = font.render("Press Enter to Play", True, WHITE)
        while True:
            self.screen.fill(BLACK)
            self.screen.blit(welcome, [SIZE[0]/2 - 200, SIZE[1]/2 - 50])
            self.screen.blit(initialize, [SIZE[0]/2 - 150, SIZE[1]/2])
            
            for asteroid in self.asteroids:
                asteroid.draw(self.screen)

            PG.display.flip()

            for event in PG.event.get():
                if event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                    return
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
    def update_bullets(self, delta):
        """Update bullets and check for collisions with asteroids"""
        for bullet in self.bullets:
            bullet.update(delta)
            wrap(bullet, ASIZE)
            for asteroid in self.asteroids:
                if abs(asteroid.center[0] - bullet.corners[0][0]) < 2 * ASIZE:
                    if collides(asteroid, bullet):
                        self.debris2.append(Debris(asteroid, ASIZE))
                        self.asteroid_die.play()
                        if asteroid.order > 1:
                            #Create smaller asteroid
                            self.asteroids.append(Asteroid(asteroid.order - 1, asteroid.center))
                            self.asteroids.append(Asteroid(asteroid.order - 1, asteroid.center))
                        self.asteroids.remove(asteroid)
                        self.score += 20
            #removes bullet if it has outlived its lifetime
            if bullet.t > BMAXT:
                    self.bullets.remove(bullet)
    def update_asteroids(self, delta):
        """updates asteroids and checks for collision with ship"""
        for asteroid in self.asteroids:
            asteroid.update(delta)
            wrap(asteroid, ASIZE)
            #Only checks for collision if objects are near each other
            if abs(asteroid.center[0] - self.enterprise.center[0]) < 2 * ASIZE and not self.enterprise.is_Invincible():
                if collides(asteroid, self.enterprise):
                    self.asteroid_die.play()
                    self.asteroids.remove(asteroid)
                    self.lives -= 1
                    self.debris.append(Debris(self.enterprise, SSIZE))
                    self.enterprise.center = array([SIZE[0] / 2, SIZE[1] / 2])
                    self.enterprise.vel = array([0, 0])
                    self.enterprise.angle = -math.pi / 2
                    self.enterprise.set_invincible()

    def update_all(self):
        """Updates all objects"""
        delta = self.clock.tick() / 1000.0
        self.enterprise.update(delta)
        wrap(self.enterprise, SSIZE)
        
        self.update_bullets(delta)
        for item in self.debris:
            item.update(delta)
            if item.t > DMAXT:
                self.debris.remove(item)

        for item in self.debris2:
            item.update(delta)
            if item.t > DMAXT:
                self.debris2.remove(item)

        for tb in self.thrustballs:
            tb.update(delta)
            if tb.t > TMAXT:
                self.thrustballs.remove(tb)

        self.update_asteroids(delta)

    def play(self):
        """Plays the game, returns after the player dies"""
        while True:
            self.clock.tick(FPS)
            self.time_since_press += self.clock.get_time()
            self.screen.fill(BLACK)
            font = PG.font.SysFont('Calibri', 25, True, False)
            scoreboard = font.render("SCORE: " + str(self.score), True, WHITE)
            numlives = font.render("LIVES: " + str(self.lives), True, WHITE)
            level = font.render("LEVEL: " + str(self.levelnum), True, WHITE)
            self.screen.blit(scoreboard, [0, 0])
            self.screen.blit(numlives, [0, 25])
            self.screen.blit(level, [SIZE[0]-100, 0])

            #Draws all items on screen
            allItems = self.asteroids+self.bullets+self.thrustballs+self.debris+self.debris2
            for item in allItems:
                item.draw(self.screen)

            #if debris is empty then the ship is still alive
            if self.debris == []:
                self.enterprise.draw(self.screen)

            PG.display.flip()

            self.update_all()

            if self.lives == 0:
                return
            if self.asteroids == []:
                #Move to next level
                self.levelnum += 1
                for i in range(ASTEROIDS + self.levelnum):
                    self.asteroids.append(Asteroid())
                self.enterprise.set_invincible

            """USER INPUT"""
            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_p:
                    self.pause()

            keys = PG.key.get_pressed()
            if keys[PG.K_RIGHT]:
                self.enterprise.turn(math.pi/45)
            if keys[PG.K_LEFT]:
                self.enterprise.turn(-math.pi/45)
            if keys[PG.K_DOWN]:
                self.enterprise.accelerate(-.1)
            if keys[PG.K_UP]:
                if self.debris == []:
                    self.thrustballs.append(Thrust(self.enterprise))
                    self.thrustballs.append(Thrust(self.enterprise))
                    self.thrustballs.append(Thrust(self.enterprise))
                    self.enterprise.accelerate(.1)
            if keys[PG.K_SPACE]:
                if self.time_since_press > TIME_TO_PRESS and self.debris == []:
                    self.shoot.play()
                    self.bullets.append(Missile(self.enterprise))
                    self.time_since_press = 0

    def game_over(self):
        """Shows players score, returns true to play again or false otherwise"""
        self.screen.fill(WHITE)
        font = PG.font.SysFont('Helvitica', 50, True, False)
        final = font.render("GAME OVER", True, BLACK)
        scoreboard = font.render("YOUR SCORE: " + str(self.score), True, BLACK)
        question = font.render("Play Again? Y/N", True, BLACK)
        self.screen.blit(final, [SIZE[0]/2 - 150, SIZE[1]/2 - 50])
        self.screen.blit(scoreboard, [SIZE[0]/2 - 175, SIZE[1]/2])
        self.screen.blit(question, [SIZE[0]/2 - 175, SIZE[1]/2 + 50])

        PG.display.flip()
        while True:
            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_y:
                    #Play again
                    return True
                if event.type == PG.KEYDOWN and event.key == PG.K_n:
                    #Don't play again
                    return False
    def pause(self):
        """Game stays here until player quits the game or resumes play"""
        self.screen.fill(WHITE)
        font = PG.font.SysFont('Helvitica', 50, True, False)
        pause = font.render("GAME PAUSED", True, BLACK)
        command = font.render("PRESS P TO CONTINUE", True, BLACK)
        self.screen.blit(pause, [SIZE[0]/2 - 150, SIZE[1]/2])
        self.screen.blit(command, [SIZE[0]/2 - 225, SIZE[1]/2 + 50])

        PG.display.flip()
        while True:
            for event in PG.event.get():
                if event.type == PG.QUIT:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                    PG.quit()
                    exit()
                if event.type == PG.KEYDOWN and event.key == PG.K_p:
                    #Unpause
                    return


def main():
    game = Game()
    game.run()

main()
