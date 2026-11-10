import pygame
import math
import random
WIDTH, HEIGHT = 900, 600 # screen width and height respectively
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("menu.mp3")

################ CLASSES ################
class Player:
    def __init__(self, direction = 90):
        self.health = Health(1000)
        self.radius = 20
        self.direction = direction
        self.x = WIDTH//2
        self.y = HEIGHT//2

    def keyBinding(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.x += 5*math.cos(self.direction)
            self.y += 5*math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x -= 5*math.cos(self.direction)
                self.y -= 5*math.sin(self.direction)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.x -= 3*math.cos(self.direction)
            self.y -= 3*math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x += 3*math.cos(self.direction)
                self.y += 3*math.sin(self.direction)

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.direction -= math.radians(5)
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.direction += math.radians(5)

    def draw(self):
        pygame.draw.circle(screen, "cyan", (self.x, self.y), self.radius)

        self.health.draw(self.x, self.y, self.radius)

        pygame.draw.line(screen,"white",(self.x, self.y),
                         (self.x + self.radius * math.cos(self.direction),
                          self.y + self.radius * math.sin(self.direction)), 3)

        # pygame.draw.circle(screen,"orange",
        #                  (self.x + 1.5 * self.radius * math.cos(self.direction),
        #                   self.y + 1.5 * self.radius * math.sin(self.direction)), 5)


class Enemy:
    def __init__(self):
        self.radius = 30
        self.health = Health(50)
        self.x = random.randint(self.radius , WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)

     ######## Spawn fix ########   
        while math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2) < self.radius + 20:
            self.x = random.randint(self.radius , WIDTH - self.radius)
            self.y = random.randint(self.radius, HEIGHT - self.radius)            

    def draw(self):
        pygame.draw.circle(screen, (246, 206, 70), (self.x, self.y), self.radius)

        self.health.draw(self.x, self.y, self.radius)


class Button:
    def __init__(self, x, y, function):
        self.x = x
        self.y = y
        self.function = function
        self.state = pygame.image.load("off.png")

    def draw(self):

        button = pygame.Surface.blit(screen, self.state, self.state.get_rect(center = (self.x, self.y)))
        if button.collidepoint(pygame.mouse.get_pos()):
            self.state = pygame.image.load("on.png")
        else:
            self.state = pygame.image.load("off.png")

class Projectile:
    def __init__(self):
        self.dir = player.direction
        self.x = player.x + 10 * math.cos(self.dir)
        self.y = player.y + 10 * math.sin(self.dir)
        self.radius = 5
        self.acceleration = 0.2
        self.base_speed = 4
        self.speed = self.base_speed
        self.max_speed = 18

    def shoot(self):
        if self.speed + self.acceleration < self.max_speed:
            self.speed += self.acceleration
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        pygame.draw.circle(screen, "purple", (self.x, self.y), self.radius)

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

    def percent(self):
        return self.current / self.max

    def draw(self, x, y, r):
        pygame.draw.rect(screen, "red", (x - 30, y - 1.5 * r, 60, 5))
        pygame.draw.rect(screen, "green", (x - 30, y - 1.5 * r, 60 * self.percent(), 5))
    
################ Functions ################
def collision(x, y, radius):
    return (
        0 > x - radius or
        x + radius > WIDTH or
        0 > y - radius or
        y + radius > HEIGHT)
######## Main Game Loop ########
def menu():
    running = True
    play = Button(WIDTH//2, HEIGHT//2, game)
    # text_surf = pygame.font.Font(None, 30)
    # text_surf.render("i on cur", text_surf, (0, 0, 0))
    # pygame.Surface.blit(screen, text_surf, )
    while running:
        clock.tick(60)
        screen.fill((62, 131, 161))
        pygame.draw.polygon(screen, "black", [(0,0), (0, HEIGHT), (WIDTH, HEIGHT)])
        play.draw()
        if pygame.mouse.get_pressed():
        # self.function()
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_0]:
                return game()
        pygame.display.flip()

def game():
    running = True
    global player
    player = Player()
    enemies = []
    projectiles = []
    for i in range (5):
        enemies.append(Enemy())

    last_shot_time = 0
    COOLDOWN = 250
    while running:

        clock.tick(60)
        start = pygame.time.get_ticks()
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for enemy in enemies:
            enemy.draw()
        for projectile in projectiles:
            projectile.shoot()
            if collision(projectile.x, projectile.y, projectile.radius):
                projectiles.remove(projectile)

        current_time = pygame.time.get_ticks()

        if current_time - last_shot_time > COOLDOWN:
            projectiles.append(Projectile())
            last_shot_time = current_time

        player.draw()
        player.health.change_health(0)
        player.keyBinding()
        pygame.display.flip()

clock = pygame.time.Clock()
pygame.mixer.music.play(loops = 4)
for i in range(40):
    pygame.mixer.music.set_volume(0.5)
    # print(pygame.mixer.music.get_volume())

# menu()
game()

pygame.quit() # closes pygame window once loop ends