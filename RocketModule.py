import pygame
import numpy as np
from RocketConstants import *

class Game:

    @staticmethod
    def checkCollision(asteroidSystem, missileSystem, rocket):

        masterSystem = []

        masterSystem.extend(asteroidSystem.system)
        masterSystem.extend(missileSystem.system)
        masterSystem.append(rocket)

        for item1 in masterSystem:
            for item2 in masterSystem:
                if item1 != item2:
                    min_dist = item1.RADIUS + item2.RADIUS 
                    dist_actual = np.sqrt((item1.x - item2.x) ** 2 + (item1.y - item2.y) ** 2)
                    if dist_actual <=  min_dist:
                        if rocket == item1 or rocket == item2:
                            return True
                        else:
                            asteroidSystem.delete(item1)
                            asteroidSystem.delete(item2)
                            missileSystem.delete(item1)
                            missileSystem.delete(item2)

        
        return False

    @staticmethod
    def run():
        
        pygame.init()
        SURFACE = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Asteroids...')
        clock = pygame.time.Clock()

            #sprite initialization
        missileSystem = MissileSystem()
        rocket = Rocket(800, 600, missileSystem, SURFACE)
        asteroidSystem = AsteroidSystem(SURFACE)
    
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
            asteroidSystem.update()


            if Game.checkCollision(asteroidSystem, missileSystem, rocket):
                gameOn = False

            clock.tick(30)
            pygame.display.update()
            count += 1


class CircleObject:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0

class AsteroidSystem(CircleObject):

    system = []

    def __init__(self, SURFACE):
        self.SURFACE = SURFACE

    def draw(self):
        for i in self.system:
            i.draw()

    def update(self):
        if len(self.system) < 5:
            
            listo = []

            #topstart
            xStart = np.random.randint(0, display_width)
            yStart = 0
            listo.append((xStart, yStart))
            #bottomstart
            xStart = np.random.randint(0, display_width)
            yStart = display_height
            listo.append((xStart, yStart))
            #leftstart
            xStart = 0
            yStart = np.random.randint(0, display_height)
            listo.append((xStart, yStart))
            #rightstart
            xStart = display_width
            yStart = np.random.randint(0, display_height)
            listo.append((xStart, yStart))

            choice = np.random.choice(range(0,len(listo)))

            xSpeed = np.random.randint(-1 * MAX_SPEED, MAX_SPEED/1.5)
            ySpeed = np.random.randint(-1 * MAX_SPEED, MAX_SPEED/1.5)

            self.system.append(Asteroid(*listo[choice], xSpeed, ySpeed, self.SURFACE))

        for asteroid in self.system:
            asteroid.update()
        
        self.draw()

    def delete(self, item):
        if item in self.system:

            R = item.RADIUS

            if item.RADIUS > 25:

                S = self.SURFACE

                a1Speed = (np.random.randint(0,5), np.random.randint(0,5))
                a2Speed = (np.random.randint(0,5), -1 * np.random.randint(0,5))
                a3Speed = (-1 * np.random.randint(0,5), np.random.randint(0,5))
                a4Speed = (-1 * np.random.randint(0,5), -1 * np.random.randint(0,5))
                
                a1 = Asteroid(item.x + R, item.y + R, *a1Speed, S, 20)
                a2 = Asteroid(item.x + R, item.y - R, *a2Speed, S, 20)
                a3 = Asteroid(item.x - R, item.y + R, *a3Speed, S, 20)
                a4 = Asteroid(item.x - R, item.y - R, *a4Speed, S, 20)

                self.system.extend([a1, a2, a3, a4])

            self.system.remove(item)


class Asteroid(CircleObject):

    def generatePoints(self):

        np.random.seed(self.SEED)

        x = self.x
        y = self.y
        rad = self.RADIUS
        thetas = np.linspace(0 , 2 * np.pi , 9)
        xRands = [-1 * np.random.randint(0, rad/5) for i in range(len(thetas))]
        yRands = [-1 * np.random.randint(0, rad/5) for i in range(len(thetas))]
        xs = (self.RADIUS * np.cos(thetas)) + x
        ys = (self.RADIUS * np.sin(thetas)) + y
        xs += xRands
        ys += yRands

        points = zip(xs,ys)

        return list(points)
        
    def __init__(self, x, y, xVel, yVel, SURFACE, radius=None):
        super().__init__(x, y)
        self.xVel = xVel
        self.yVel = yVel
        self.SURFACE = SURFACE
        self.SEED = np.random.randint(0, 100) # 100 possible asteroids
        if radius == None:
            self.RADIUS = np.random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        else:
            self.RADIUS = radius
        self.points = self.generatePoints()

 

    def draw(self):
        
        pygame.draw.polygon(self.SURFACE, WHITE, self.points, 2)


    def update(self):

        self.draw()

        self.x += self.xVel
        self.y += self.yVel

        self.points = self.generatePoints()

        self.x = self.x % (display_width)
        self.y = self.y % (display_height)
        
        

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

    system = []

    def update(self):

        missiles = []
        for missile in self.system:
            
            missile.update()

            if missile.x < display_width and missile.x > 0:
                missiles.append(missile)

        self.system = missiles

    def delete(self, item):
        if item in self.system:
            self.system.remove(item)

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
            missXVel = np.cos(self.tip * R_CON)/self.RADIUS *1000
            missYVel = np.sin(self.tip * R_CON)/self.RADIUS *1000
            
            newMissile = Missile(tipLoc[0], tipLoc[1], missXVel, missYVel, self.tip, SURFACE)
            

            self.missileSystem.system.append(newMissile)


    def update(self, count, SURFACE):

        keys = pygame.key.get_pressed()

        self.x = self.x % display_width
        self.y = self.y % display_height
        
        self.tip -= (keys[pygame.K_a] - keys[pygame.K_d]) * 8
        tip = self.tip
        self.xVel += np.cos(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR
        self.yVel += np.sin(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR

        self.checkSpeed()

        self.x += self.xVel 
        self.y += self.yVel

        self.checkLaunch(count)

        self.draw(count, SURFACE)