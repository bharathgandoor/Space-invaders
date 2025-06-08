import pygame                                                                                                   ##Imports
import random
import time

pygame.init()                                                                                                   ##Initialize Pygame Window
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Space Invaders")

class Character:                                                                                                ##Parent Class "Character"
    def __init__(self, x, y, length, width, color):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color
    def draw(self):                                                                                             ##Draw Character
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.width))

class Alien(Character):                                                                                         ##Child Class "Alien"
    def movealien(self, change):
        self.x += change

class Spaceship(Character):                                                                                     ##Child Class "Spaceship"
    def movealien(self, left, right):
        if left == True:
            self.x -= 5
        if right == True:
            self.x += 5

class Bullet:                                                                                                   ##Bullet Class
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.active = True                                                                                      ##Check if bullet is active
    def move(self):                                                                                             ##Move Bullet
        self.y -= self.speed
    def draw(self):                                                                                             ##Draw Bullet
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

change = 3                                                                                                      ##Set "change" Value

AlienList = []                                                                                                  ##10 Aliens List

x = 520                                                                                                         ##Start X Position
y = 50                                                                                                          ##Start Y Position
row_length = 10                                                                                                 ##Row Length
alien_width = 75                                                                                                ##Alien Width
alien_gap = 10                                                                                                  ##Gap Between Aliens
x_offset = alien_width + alien_gap                                                                              ##X Offset Between Aliens

for i in range(1, 31):                                                                                          ##Create Aliens
    alien1 = Alien(x, y, alien_width, alien_width, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    AlienList.append(alien1)                                                                                    ##Add Alien to List

    x += x_offset                                                                                               ##Move X Position
    if i % row_length == 0:                  
        x = 520                                                                                                 ##Reset X to Start
        y += x_offset                                                                                           ##Move Y Down by Offset

spaceship = Spaceship(920, 900, 140, 60, (255, 0, 0))
left = False
right = False
space = False
bullets = []                                                                                                    ##Bullet List

clock = pygame.time.Clock()                                                                                     ##Clock for Frame Rate

def Score(msg, x, y, color, size):
    fontobj = pygame.font.SysFont("Freesans", size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))

score = 0

while True:
    screen.fill((0, 0, 0))                                                                                      ##Black Background

    spaceship.draw()                                                                                            ##Draw Spaceship
    spaceship.movealien(left, right)
    Score("Score:"  + str(score), 1750, 10, (0,0,255), 32)
    
    for bullet in bullets:                                                                                      ##Move and Draw Bullets
        if bullet.active:
            bullet.move()
            bullet.draw()
            for alien in AlienList:                                                                             ##Check Collision with Aliens
                if (
                    bullet.x < alien.x + alien.width and
                    bullet.x + bullet.width > alien.x and
                    bullet.y < alien.y + alien.width and
                    bullet.y + bullet.height > alien.y
                ):
                    AlienList.remove(alien)                                                                      ##Remove Alien
                    bullet.active = False                                                                        ##Disable Bullet
                    score+=1
                    if score == 30:
                        screen.fill((0,0,0))
                        Score("YOU WIN!", 700, 500, (0,255,0), 100)
                        pygame.display.update()
                        time.sleep(5)
                        pygame.quit()
                    break 

    bullets = [bullet for bullet in bullets if bullet.active and bullet.y > 0]                                   ##Remove Inactive Bullets

    for n in range(len(AlienList)):                                                                              ##Move and Draw Aliens
        AlienList[n].movealien(change)
        AlienList[n].draw()
    for a in range(len(AlienList)):
        if AlienList[a].x + AlienList[a].width >= 1920 or AlienList[a].x <= 0:
            change = -change
            for alien in AlienList:
                alien.y += 100
                if alien.y >= 750:
                    screen.fill((0,0,0))
                    Score("YOU LOSE!", 700, 500, (255,0,0), 100)
                    pygame.display.update()
                    time.sleep(5)
                    pygame.quit()
            break

    pygame.display.update()
    clock.tick(60)                                                                                               ##Cap frame rate to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_SPACE:
                space = True                                                                                     ##Space Key Pressed
                bullet = Bullet(spaceship.x + spaceship.length // 2 - 5, spaceship.y, 10, 20, (255, 255, 0), 10) ##Create Bullet
                bullets.append(bullet)                                                                           ##Add Bullet to List
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

        if event.type == pygame.QUIT:                                                                           ##Quit Event                        
            pygame.quit()
            exit()
