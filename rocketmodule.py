import pygame
import numpy as np
from rocketconstants import *

class Game:

    '''A class to handle the Game'''
    
    pygame.init()
    info = pygame.display.Info()
    HEIGHT = info.current_h/1.5
    WIDTH = info.current_w/1.5

    def __init__(self):
        self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Rocket')
        self.clock = pygame.time.Clock()
        self.fontEnd = pygame.font.SysFont('timesnewroman', 300)
        self.fontLife = pygame.font.SysFont('timesnewroman', 100)
        self.fontDuring = pygame.font.SysFont('timesnewroman', 100)
        self.lives = 3
        self.score = 0

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
        masterSystem.append(self.UFO)

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
                        elif self.UFO == item1 or self.UFO == item2:
                            if self.UFO == item1 and type(item2) == Asteroid:
                                self.asteroidSystem.delete(item2)
                            elif self.UFO == item2 and type(item1) == Asteroid:
                                self.asteroidSystem.delete(item1)
                            elif self.UFO == item1 and type(item2) == Missile:
                                if type(item2.origin) == Rocket:
                                    self.missileSystem.delete(item2)
                                    self.UFO.lives -= 1
                                    if self.UFO.lives == 0:
                                        self.UFO.x = -3000
                                        self.UFO.lives = self.UFO.deathCount * 5
                            elif self.UFO == item2 and type(item1) == Missile:
                                if type(item1.origin) == Rocket:
                                    self.missileSystem.delete(item1)
                                    self.UFO.lives -= 1
                                    self.UFO.deathCount += 1
                                    if self.UFO.lives == 0:
                                        self.UFO.x = -3000
                                        self.UFO.lives = self.UFO.deathCount * 3
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
            playAgain = self.fontDuring.render("Press spacebar to play again.",
                                                False, WHITE, BLACK)
            self.SURFACE.blit(scoreMessage, (self.info.current_w/40,
                                            self.info.current_h/40))
            self.SURFACE.blit(score, (self.info.current_w/3, self.info.current_h/5))
            self.SURFACE.blit(playAgain, (self.info.current_w/10, 
                                                self.info.current_h/2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1:
                wait = False
                self.score = 0
                self.lives = 4 # reset will subtract 1
                self.reset()
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
        self.rocket = Rocket(800, 600, self.missileSystem, self.SURFACE, 25)
        self.UFO = UFO(0, 200, self.missileSystem, self.SURFACE, 80, 
                                self.rocket)
        self.asteroidSystem = AsteroidSystem(self.SURFACE)

    def reset(self):
        '''A method to reset the game sprites'''
        self.setup()
        self.lives -= 1
        self.asteroidSystem.system = []

    def displayLives(self):
        '''A method to display lives in the top right corner.'''
        x = Game.WIDTH*.85
        y = 200
        for i in range(self.lives):
            rocket = Rocket(x, y, MissileSystem(), self.SURFACE, 50)
            rocket.tip = 270
            rocket.draw(2)
            x += 75
    
    def pause(self):
        '''A method to pause the game'''
        pygame.time.wait(1000)
        while not self.eventListener():
            pause = self.fontLife.render("Press spacebar to continue...", 
                                            False, WHITE, BLACK)
            self.SURFACE.blit(pause, (Game.WIDTH/5, Game.HEIGHT/3))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1:
                self.setup()
                self.lives -= 1
                break

    def run(self):
        self.setup()
        count = 0
        gameOn = True
        while gameOn:
            gameOn = not self.eventListener()

            self.SURFACE.fill(BLACK)

            self.UFO.update()
            self.rocket.update(count)
            self.missileSystem.update()
            self.asteroidSystem.update()

            if self.checkCollision():
                if self.lives == 0:
                    self.displayEnd()
                else:
                    self.pause()

            self.displayScore()
            self.displayLives()

            self.clock.tick(60)
            pygame.display.flip()
            count += 1 % 20000

class CircleObject:

    '''A base class for every sprite to inherit from'''

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0

class AsteroidSystem(CircleObject):

    '''A class for handling sstems of asteroids'''

    def __init__(self, SURFACE):
        '''A method to initialize the AsteroidSystem Class'''
        self.system = []
        self.SURFACE = SURFACE

    def draw(self):
        '''A method to draw the asteroids contained in the system'''
        for asteroid in self.system:
            asteroid.draw()

    def generateXYStart(self):
        listo = []
        #topstart
        xStart = np.random.randint(0, Game.WIDTH)
        yStart = 0
        listo.append((xStart, yStart))
        #bottomstart
        xStart = np.random.randint(0, Game.WIDTH)
        yStart = Game.HEIGHT
        listo.append((xStart, yStart))
        #leftstart
        xStart = 0
        yStart = np.random.randint(0, Game.HEIGHT)
        listo.append((xStart, yStart))
        #rightstart
        xStart = Game.WIDTH
        yStart = np.random.randint(0, Game.HEIGHT)
        listo.append((xStart, yStart))
        return listo

    def update(self):
        '''A method to update the asteroid system'''
        if len(self.system) < 20:
            
            listo = self.generateXYStart()
            choice = np.random.choice(range(0,len(listo)))
            xSpeed = np.random.randint(-1 * MAX_SPEED/1.1, MAX_SPEED/1.1)
            ySpeed = np.random.randint(-1 * MAX_SPEED/1.1, MAX_SPEED/1.1)
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

                a1Speed = (np.random.randint(0,MAX_SPEED/1.1), np.random.randint(0,MAX_SPEED/1.1))
                a2Speed = (np.random.randint(0,MAX_SPEED/1.1), -1 * np.random.randint(0,MAX_SPEED/1.1))
                a3Speed = (-1 * np.random.randint(0,MAX_SPEED/1.1), np.random.randint(0,MAX_SPEED/1.1))
                a4Speed = (-1 * np.random.randint(0,MAX_SPEED/1.1), -1 * np.random.randint(0,MAX_SPEED/1.1))
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

        self.x = self.x % (Game.WIDTH)
        self.y = self.y % (Game.HEIGHT)

class Missile(CircleObject):
    '''A class to work with missiles'''
    RADIUS = 1

    def __init__(self, x, y, xVel, yVel, tip, SURFACE, origin, target=None):
        '''A class to initialize the missile object'''
        super().__init__(x, y)
        self.xVel = xVel
        self.yVel = yVel
        self.tip = tip
        self.SURFACE = SURFACE
        self.origin = origin
        self.target = target

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
        if self.target:
            selfVec = np.array([self.x, self.y])
            rocketVec = np.array([self.target.x, self.target.y])
            dist = rocketVec - selfVec
            nDist = dist / np.linalg.norm(dist) * MAX_SPEED
            self.x += nDist[0]
            self.y += nDist[1]
        else:
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

            if missile.x < Game.WIDTH and missile.x > 0:
                if missile.y < Game.HEIGHT and missile.y > 0:
                    missiles.append(missile)

        self.system = missiles

    def delete(self, item):
        '''A method to delete a missile'''
        if item in self.system:
            self.system.remove(item)

class UFO(CircleObject):

    '''A class for working with UFO's'''

    def __init__(self, x, y, missileSystem, SURFACE, RADIUS, rocket):
        super().__init__(x, y)
        self.missileSystem = missileSystem
        self.SURFACE = SURFACE
        self.tip = 0
        self.RADIUS = RADIUS
        self.lives = 5
        self.currTime = pygame.time.get_ticks()
        self.rocket = rocket
        self.deathCount = 0

    def update(self):
        if self.x < Game.WIDTH/2 - 10:
            self.x += 5 
        #self.x = self.x % Game.WIDTH
        rocket = self.rocket
        if (pygame.time.get_ticks() - self.currTime) >= 1000:
            self.currTime = pygame.time.get_ticks()
            selfVec = np.array([self.x, self.y])
            rocketVec = np.array([rocket.x, rocket.y])
            dist = rocketVec - selfVec
            nDist = dist / np.linalg.norm(dist) * MAX_SPEED
            missile = Missile(self.x, self.y, *nDist, 180, self.SURFACE, self)
            self.missileSystem.system.append(missile)

        self.draw()

    def draw(self):
        if self.lives > 3:
            pygame.draw.circle(self.SURFACE, WHITE, (self.x, self.y), self.RADIUS, 1)
        innerRect = pygame.Rect(self.x-self.RADIUS + 5, self.y, 150, 35)
        arcRect = pygame.Rect(self.x-28, self.y - 25, 60, 60)
        pygame.draw.arc(self.SURFACE, WHITE, arcRect, 0, np.pi, 2)
        pygame.draw.ellipse(self.SURFACE, WHITE, innerRect, 7)
    
class Rocket(CircleObject):

    '''A class for working with the player's rocket'''

    def __init__(self, x, y, missileSystem, SURFACE, radius):
        super().__init__(x, y)
        self.missileSystem = missileSystem
        self.SURFACE = SURFACE
        self.tip = 0
        self.RADIUS = radius
        self.time_ = 0
        self.prev_time = 0
        self.threshold = 0

    def getTipLoc(self):
        return (self.x + self.RADIUS * np.cos(self.tip * R_CON), 
                self.y + self.RADIUS * np.sin(self.tip * R_CON))
    
    def getLeftLoc(self):
        return (self.x + self.RADIUS * np.cos((self.tip + 210) * R_CON), 
                self.y + self.RADIUS * np.sin((self.tip + 210)* R_CON))

    def getRightLoc(self):
        return (self.x + self.RADIUS * np.cos((self.tip + 150) * R_CON), 
                self.y + self.RADIUS * np.sin((self.tip + 150) * R_CON))

    def draw(self, count):
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
        self.currTime = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] == 1 and self.currTime > self.threshold:
            self.threshold = self.currTime + 200
            tipLoc = (self.x + self.RADIUS * np.cos(self.tip * R_CON), 
                      self.y + self.RADIUS * np.sin(self.tip * R_CON))
            missXVel = np.cos(self.tip * R_CON)/self.RADIUS *1000
            missYVel = np.sin(self.tip * R_CON)/self.RADIUS *1000
            
            newMissile = Missile(tipLoc[0], tipLoc[1], missXVel, missYVel, 
                                    self.tip, SURFACE, self)
            self.missileSystem.system.append(newMissile)

    def update(self, count):
        '''A method to update the rocket objet on screen'''
        keys = pygame.key.get_pressed()

        self.x = self.x % Game.WIDTH
        self.y = self.y % Game.HEIGHT
        
        self.tip -= (keys[pygame.K_a] - keys[pygame.K_d]) * ROT_SPEED
        tip = self.tip
        self.xVel += np.cos(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR
        self.yVel += np.sin(tip * R_CON) * keys[pygame.K_w]/self.RADIUS * ACC_FACTOR

        self.checkSpeed()

        self.x += self.xVel 
        self.y += self.yVel

        self.checkLaunch(count)

        self.draw(count)