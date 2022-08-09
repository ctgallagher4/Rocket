from turtle import window_height, window_width
import pygame
import numpy as np
from RocketConstants import *



class Game:
    @staticmethod
    def run():
        
        pygame.init()
        SURFACE = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Asteroids...')
        clock = pygame.time.Clock()

            #sprite initialization
        missileSystem = MissileSystem()
        rocket = Rocket(800, 600, missileSystem, SURFACE)
        asteroid = Asteroid(500, 400, 4, 4, SURFACE)
    
        count = 0
        gameOn = True
        while gameOn:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # quit the screen
                    gameOn = False

            SURFACE.fill(BLACK)

            rocket.update(count, SURFACE)
            missileSystem.update()
            asteroid.update()

            clock.tick(30)
            pygame.display.update()
            count += 1


class CircleObject:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0 

class Asteroid(CircleObject):

    RADIUS = np.random.randint(50, 100)

    def generatePoints(self):

        np.random.seed(self.SEED)

        x = self.x
        y = self.y
        rad = self.RADIUS
        thetas = np.linspace(0 , 2 * np.pi , 10)
        xRands = [-1 * np.random.randint(0, rad/5) for i in range(len(thetas))]
        yRands = [-1 * np.random.randint(0, rad/5) for i in range(len(thetas))]
        xs = (self.RADIUS * np.cos(thetas)) + x
        ys = (self.RADIUS * np.sin(thetas)) + y
        xs += xRands
        ys += yRands

        points = zip(xs,ys)

        return list(points)
        
    def __init__(self, x, y, xVel, yVel, SURFACE):
        super().__init__(x, y)
        self.xVel = xVel
        self.yVel = yVel
        self.SURFACE = SURFACE
        self.SEED = np.random.randint(0, 100) # 100 possible asteroids
        self.points = self.generatePoints()

 

    def draw(self):

        
        
        pygame.draw.polygon(self.SURFACE, WHITE, self.points, 2)


    def update(self):

        self.draw()

        self.x += self.xVel
        self.y += self.yVel

        self.points = self.generatePoints()

        self.x = self.x % display_width
        self.y = self.y % display_height
        
        

class Missile(CircleObject):

    RADIUS = 1


    def __init__(self, x, y, xVel, yVel, tip, SURFACE):
        super().__init__(x, y)
        self.xVel = xVel
        self.yVel = yVel
        self.tip = tip
        self.SURFACE = SURFACE


    def draw(self):
        SURFACE = self.SURFACE
        topLeftLoc = (self.x + self.RADIUS * np.cos((self.tip + 30) * R_CON), 
                  self.y + self.RADIUS * np.sin((self.tip + 30) * R_CON))
        topRightLoc = (self.x + self.RADIUS * np.cos((self.tip + 330) * R_CON), 
                  self.y + self.RADIUS * np.sin((self.tip + 330) * R_CON))
        leftLoc = (self.x + self.RADIUS * np.cos((self.tip + 210) * R_CON), 
                   self.y + self.RADIUS * np.sin((self.tip + 210)* R_CON))
        rightLoc = (self.x + self.RADIUS * np.cos((self.tip + 150) * R_CON), 
                   self.y + self.RADIUS * np.sin((self.tip + 150) * R_CON))
        pygame.draw.polygon(SURFACE, WHITE, [topLeftLoc, topRightLoc, leftLoc,
                            rightLoc])

    def update(self):

        self.draw()

        self.x += self.xVel
        self.y += self.yVel

class MissileSystem:

    missiles = []

    def update(self):

        missiles = []
        for missile in self.missiles:
            
            missile.update()

            if missile.x < display_width and missile.x > 0:
                missiles.append(missile)

        self.missiles = missiles

class Rocket(CircleObject):

    RADIUS = 25
    tip = 0 # degrees

    def __init__(self, x, y, missileSystem, SURFACE):
        super().__init__(x, y)
        self.missileSystem = missileSystem
        self.SURFACE = SURFACE

    def getTipLoc(self):
        return (self.x + self.RADIUS * np.cos(self.tip * R_CON), 
                self.y + self.RADIUS * np.sin(self.tip * R_CON))
    
    def getLeftLoc(self):
        return (self.x + self.RADIUS * np.cos((self.tip + 210) * R_CON), 
                self.y + self.RADIUS * np.sin((self.tip + 210)* R_CON))

    def getRightLoc(self):
        return (self.x + self.RADIUS * np.cos((self.tip + 150) * R_CON), 
                self.y + self.RADIUS * np.sin((self.tip + 150) * R_CON))

    def draw(self, count, SURFACE):
        SURFACE = self.SURFACE
        triangle = [self.getTipLoc(), self.getLeftLoc(), self.getRightLoc()]
        pygame.draw.polygon(SURFACE, WHITE, triangle, 1)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] == 1 and count % 5 == 0:
            flameTipLoc = (self.x + self.RADIUS * -1.5 * np.cos(self.tip * R_CON), 
                           self.y + self.RADIUS * -1.5 * np.sin(self.tip * R_CON))
            flameLeftLoc = triangle[1]
            flameRightLoc = triangle[2]
            newList = [flameTipLoc, flameLeftLoc, flameRightLoc]
            pygame.draw.polygon(SURFACE, WHITE, newList)

    def checkSpeed(self):
        if self.xVel > MAX_SPEED:
            self.xVel = MAX_SPEED
        if self.xVel < -1 * MAX_SPEED:
            self.xVel = -1 * MAX_SPEED
        if self.yVel > MAX_SPEED:
            self.yVel = MAX_SPEED
        if self.yVel < -1 * MAX_SPEED:
            self.yVel = -1 * MAX_SPEED

    def checkLaunch(self, count):

        SURFACE = self.SURFACE

        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_SPACE] == 1 and count % 7 == 0:
            tipLoc = (self.x + self.RADIUS * np.cos(self.tip * R_CON), 
                  self.y + self.RADIUS * np.sin(self.tip * R_CON))
            missXVel = np.cos(self.tip * R_CON)/self.RADIUS * 1000 + self.xVel
            missYVel = np.sin(self.tip * R_CON)/self.RADIUS * 1000 + self.yVel
            newMissile = Missile(*tipLoc, missXVel, missYVel, self.tip, SURFACE)

            self.missileSystem.missiles.append(newMissile)


    def update(self, count, SURFACE):

        keys = pygame.key.get_pressed()

        self.x = self.x % display_width
        self.y = self.y % display_height
        
        self.tip -= (keys[pygame.K_a] - keys[pygame.K_d]) * 8
        tip = self.tip
        self.xVel += np.cos(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * 6
        self.yVel += np.sin(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * 6

        self.checkSpeed()

        self.x += self.xVel 
        self.y += self.yVel

        self.checkLaunch(count)

        self.draw(count, SURFACE)