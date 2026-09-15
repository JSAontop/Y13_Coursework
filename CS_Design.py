import pygame
import math
import random
WIDTH, HEIGHT = 900, 600 # screen width and height respectively
screen = pygame.display.set_mode((WIDTH, HEIGHT))

################ Functions ################
def collision(x, y, radius):
    return (
        0 > x - radius or
        x + radius > WIDTH or
        0 > y - radius or
        y + radius > HEIGHT)

################ CLASSES ################
class Player:
    def __init__(self, direction = 90):
        self.health = Health(100)
        self.radius = 20
        self.direction = direction
        self.x = WIDTH//2
        self.y = HEIGHT//2

    def input_handling(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.x += 5*math.cos(self.direction)
            self.y += 5*math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x -= 5*math.cos(self.direction)
                self.y -= 5*math.sin(self.direction)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.x -= 5*math.cos(self.direction)
            self.y -= 5*math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x += 5*math.cos(self.direction)
                self.y += 5*math.sin(self.direction)

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.direction -= math.radians(5)
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.direction += math.radians(5)

    def draw(self):
        pygame.draw.circle(screen, "cyan", (self.x, self.y), self.radius)

        pygame.draw.line(screen,"white",(self.x, self.y),
                         (self.x + self.radius * math.cos(self.direction),
                          self.y + self.radius * math.sin(self.direction)), 3)

        # pygame.draw.circle(screen,"orange",
        #                  (self.x + 1.5 * self.radius * math.cos(self.direction),
        #                   self.y + 1.5 * self.radius * math.sin(self.direction)), 5)


class Enemy:
    def __init__(self):
        self.radius = 30
        self.x = random.randint(self.radius , WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)

     ######## Spawn fix ########   
        while math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2) < self.radius + 20:
            self.x = random.randint(self.radius , WIDTH - self.radius)
            self.y = random.randint(self.radius, HEIGHT - self.radius)            

    def draw(self):
        pygame.draw.circle(screen, "red", (self.x, self.y), self.radius)

class Health:
    def __init__(self, MAX):
        self.max = MAX
        self.current = MAX

    def change_health(self, change):
        self.current += change
        if self.current < 0:
            self.current = 0
        elif self.current > self.max:
            self.current = self.max

    def draw(self):
        pass
    

######## Main Game Loop ########
player = Player()
enemies = []
for i in range (5):
    enemies.append(Enemy())

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for enemy in enemies:
        enemy.draw()
    player.draw()
    player.input_handling()
    pygame.display.flip()

pygame.quit() # closes pygame window once loop ends

