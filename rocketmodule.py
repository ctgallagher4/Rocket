import pygame
import numpy as np
from rocketconstants import *

class Game:

    def __init__(self):
        pygame.init()
        self.SURFACE = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
        pygame.display.set_caption('Asteroids...')
        self.clock = pygame.time.Clock()
        self.fontEnd = pygame.font.SysFont('timesnewroman', 300)
        self.fontDuring = pygame.font.SysFont('timesnewroman', 100)

    def updateScore(self, item1, item2):
        '''A helper method for checkCollision which updates the score'''
        if type(item1) == Missile:
            self.score += item2.RADIUS
        elif type(item2) == Missile:
            self.score += item1.RADIUS


    def checkCollision(self):
        '''A method to check for collisions between sprites'''
        masterSystem = []

        masterSystem.extend(self.asteroidSystem.system)
        masterSystem.extend(self.missileSystem.system)
        masterSystem.append(self.rocket)

        for item1 in masterSystem:
            for item2 in masterSystem:
                if item1 != item2:
                    min_dist = item1.RADIUS + item2.RADIUS 
                    dist_actual = np.sqrt(
                            (item1.x - item2.x) ** 2 + (item1.y - item2.y) ** 2
                        )
                    if dist_actual <=  min_dist:
                        if self.rocket == item1 or self.rocket == item2:
                            return True
                        else:
                            self.updateScore(item1, item2)
                            self.asteroidSystem.delete(item1)
                            self.asteroidSystem.delete(item2)
                            self.missileSystem.delete(item1)
                            self.missileSystem.delete(item2)
        return False

    def displayEnd(self):
        '''A method to display the end of Game Screen'''
        pygame.time.wait(1000)
        self.SURFACE.fill(BLACK)
        pygame.display.flip()
        wait = True
        while wait:
            wait = not self.eventListener()
            score = self.fontEnd.render(str(self.score), False, WHITE, BLACK)
            scoreMessage = self.fontEnd.render("Your Score Is: ", False, 
                                                WHITE, BLACK)
            playAgain = self.fontDuring.render("Press spacebar to play again:",
                                                False, WHITE, BLACK)
            self.SURFACE.blit(scoreMessage, (DISPLAY_WIDTH/2-900,
                                                DISPLAY_HEIGHT/2-500))
            self.SURFACE.blit(score, (DISPLAY_WIDTH/2-100, DISPLAY_HEIGHT/2-100))
            self.SURFACE.blit(playAgain, (DISPLAY_WIDTH/2 - 500, 
                                                DISPLAY_HEIGHT/2 + 300))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1:
                self.reset()
                wait = False
            pygame.display.flip()

    def eventListener(self):
        '''A method to listen for events, specifically quit'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        else:
            return False

    def displayScore(self):
        '''A method to display the score to the screen'''
        score = self.fontDuring.render(str(self.score), False, WHITE)
        self.SURFACE.blit(score, (100,100))


    def setup(self):
        '''A method to setup the game sprites'''
        self.missileSystem = MissileSystem()
        self.rocket = Rocket(800, 600, self.missileSystem, self.SURFACE)
        self.asteroidSystem = AsteroidSystem(self.SURFACE)
        self.score = 0

    def reset(self):
        '''A method to reset the game sprites'''
        self.setup()
        self.asteroidSystem.system = []

    def run(self):
        '''A method to run the game'''
        self.setup()
    
        count = 0
        gameOn = True
        while gameOn:
        
            gameOn = not self.eventListener()

            self.SURFACE.fill(BLACK)

            self.rocket.update(count, self.SURFACE)
            self.missileSystem.update()
            self.asteroidSystem.update()


            if self.checkCollision():
                self.displayEnd()

            self.displayScore()

            self.clock.tick(30)
            pygame.display.flip()
            count += 1

class CircleObject:
    '''A base class for every sprite to inherit from'''
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0

class AsteroidSystem(CircleObject):
    '''A class for handling sstems of asteroids'''
    system = []

    def __init__(self, SURFACE):
        '''A method to initialize the AsteroidSystem Class'''
        self.SURFACE = SURFACE

    def draw(self):
        '''A method to draw the asteroids contained in the system'''
        for asteroid in self.system:
            asteroid.draw()

    def update(self):
        '''A method to update the asteroid system'''
        if len(self.system) < 20:
            
            listo = []
            #topstart
            xStart = np.random.randint(0, DISPLAY_WIDTH)
            yStart = 0
            listo.append((xStart, yStart))
            #bottomstart
            xStart = np.random.randint(0, DISPLAY_WIDTH)
            yStart = DISPLAY_HEIGHT
            listo.append((xStart, yStart))
            #leftstart
            xStart = 0
            yStart = np.random.randint(0, DISPLAY_HEIGHT)
            listo.append((xStart, yStart))
            #rightstart
            xStart = DISPLAY_WIDTH
            yStart = np.random.randint(0, DISPLAY_HEIGHT)
            listo.append((xStart, yStart))

            choice = np.random.choice(range(0,len(listo)))

            xSpeed = np.random.randint(-1 * MAX_SPEED/1.5, MAX_SPEED/1.5)
            ySpeed = np.random.randint(-1 * MAX_SPEED/1.5, MAX_SPEED/1.5)

            self.system.append(Asteroid(*listo[choice], xSpeed, ySpeed, self.SURFACE))

        for asteroid in self.system:
            asteroid.update()
        
        self.draw()

    def delete(self, item):
        '''A method to delete an asteroid from the system'''
        if item in self.system:

            R = item.RADIUS

            if item.RADIUS > MAX_SMALL_SIZE:

                S = self.SURFACE

                a1Speed = (np.random.randint(0,5), np.random.randint(0,5))
                a2Speed = (np.random.randint(0,5), -1 * np.random.randint(0,5))
                a3Speed = (-1 * np.random.randint(0,5), np.random.randint(0,5))
                a4Speed = (-1 * np.random.randint(0,5), -1 * np.random.randint(0,5))
                a1Size = np.random.randint(MIN_SMALL_SIZE, MAX_SMALL_SIZE)
                a2Size = np.random.randint(MIN_SMALL_SIZE, MAX_SMALL_SIZE)
                a3Size = np.random.randint(MIN_SMALL_SIZE, MAX_SMALL_SIZE)
                a4Size = np.random.randint(MIN_SMALL_SIZE, MAX_SMALL_SIZE)
                a1 = Asteroid(item.x + R, item.y + R, *a1Speed, S, a1Size)
                a2 = Asteroid(item.x + R, item.y - R, *a2Speed, S, a2Size)
                a3 = Asteroid(item.x - R, item.y + R, *a3Speed, S, a3Size)
                a4 = Asteroid(item.x - R, item.y - R, *a4Speed, S, a4Size)

                self.system.extend([a1, a2, a3, a4])

            self.system.remove(item)

class Asteroid(CircleObject):

    '''A class for working with asteroid objects'''

    def __init__(self, x, y, xVel, yVel, SURFACE, radius=None):
        '''A method to initialize an asteroid class'''
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

    def generatePoints(self):
        '''Dynamically generates all of the points to draw for a given asteroid'''
        np.random.seed(self.SEED)
        x = self.x
        y = self.y
        rad = self.RADIUS
        thetas = np.linspace(0 , 2 * np.pi , NUMBER_OF_POINTS)
        xRands = [-1 * np.random.randint(0, rad/JAG) for i in range(len(thetas))]
        yRands = [-1 * np.random.randint(0, rad/JAG) for i in range(len(thetas))]
        xs = (self.RADIUS * np.cos(thetas)) + x
        ys = (self.RADIUS * np.sin(thetas)) + y
        xs += xRands
        ys += yRands
        points = zip(xs,ys)
        return list(points)


    def draw(self):
        '''A method to draw an asteroid'''
        pygame.draw.polygon(self.SURFACE, WHITE, self.points, 2)


    def update(self):
        '''A method to update an asteroid on screen'''
        self.draw()

        self.x += self.xVel
        self.y += self.yVel

        self.points = self.generatePoints()

        self.x = self.x % (DISPLAY_WIDTH)
        self.y = self.y % (DISPLAY_HEIGHT)

class Missile(CircleObject):
    '''A class to work with missiles'''
    RADIUS = 1

    def __init__(self, x, y, xVel, yVel, tip, SURFACE):
        '''A class to initialize the missile object'''
        super().__init__(x, y)
        self.xVel = xVel
        self.yVel = yVel
        self.tip = tip
        self.SURFACE = SURFACE

    def draw(self):
        '''A class to draw a missile'''
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
        '''A method to update a missile on the screen'''
        self.draw()

        self.x += self.xVel
        self.y += self.yVel

class MissileSystem:

    '''A class for working with multiple missiles'''

    system = []

    def update(self):
        '''A method to update the MissileSystem'''
        missiles = []
        for missile in self.system:
            
            missile.update()

            if missile.x < DISPLAY_WIDTH and missile.x > 0:
                missiles.append(missile)

        self.system = missiles

    def delete(self, item):
        '''A method to delete a missile'''
        if item in self.system:
            self.system.remove(item)

class Rocket(CircleObject):
    '''A class for working with the player's rocket'''
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
        '''A method to insure the speed of the rocket does not exceed maxes'''
        if self.xVel > MAX_SPEED:
            self.xVel = MAX_SPEED
        if self.xVel < -1 * MAX_SPEED:
            self.xVel = -1 * MAX_SPEED
        if self.yVel > MAX_SPEED:
            self.yVel = MAX_SPEED
        if self.yVel < -1 * MAX_SPEED:
            self.yVel = -1 * MAX_SPEED

    def checkLaunch(self, count):
        '''A method to check if the spacebar has launched a missile'''
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
        '''A method to update the rocket objet on screen'''
        keys = pygame.key.get_pressed()

        self.x = self.x % DISPLAY_WIDTH
        self.y = self.y % DISPLAY_HEIGHT
        
        self.tip -= (keys[pygame.K_a] - keys[pygame.K_d]) * 8
        tip = self.tip
        self.xVel += np.cos(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR
        self.yVel += np.sin(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR

        self.checkSpeed()

        self.x += self.xVel 
        self.y += self.yVel

        self.checkLaunch(count)

        self.draw(count, SURFACE)