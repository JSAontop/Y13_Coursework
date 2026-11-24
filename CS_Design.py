import pygame
import math
import random


WIDTH, HEIGHT = 900, 600 # screen width and height respectively

################ COLOURS ################
NAVY = (62, 131, 161)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("menu.mp3")

################ CLASSES ################
class Player:
    def __init__(self, direction = 0):
        self.health = Health(1000)
        self.radius = 20
        self.direction = direction
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.speed = 6

    def keyBinding(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.x += self.speed * math.cos(self.direction)
            self.y += self.speed * math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x -= self.speed * math.cos(self.direction)
                self.y -= self.speed * math.sin(self.direction)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.x -= 0.6 * self.speed * math.cos(self.direction)
            self.y -= 0.6 * self.speed * math.sin(self.direction)
            if collision(self.x, self.y, self.radius):
                self.x += 0.6 * self.speed * math.cos(self.direction)
                self.y += 0.6 * self.speed * math.sin(self.direction)

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
        overlap = 1
     ######## Spawn fix ########   
        while overlap != 0:
            self.x = random.randint(self.radius , WIDTH - self.radius)
            self.y = random.randint(self.radius, HEIGHT - self.radius)
            overlap = 0
            if math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2) < self.radius + player.radius + 10:
                overlap += 1
            for enemy in enemies:
                if math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2) < self.radius + enemy.radius + 5:
                    overlap += 1


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
        self.dir = player.direction + math.pi * random.randint(-5, 5) / 180
        self.x = player.x + 10 * math.cos(self.dir)
        self.y = player.y + 10 * math.sin(self.dir)
        self.radius = 5
        self.acceleration = 0.5
        self.speed = 8
        self.max_speed = 18

    def shoot(self):
        if self.speed + self.acceleration < self.max_speed:
            self.speed += self.acceleration
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
        pygame.draw.circle(screen, "purple", (self.x, self.y), self.radius)

class Health:
    def __init__(self, MAX, fill = "green", border = "red"):
        self.max = MAX
        self.current = MAX
        self.fill = fill
        self.border = border

    def change_health(self, change):
        self.current += change
        if self.current < 0:
            self.current = 0
        elif self.current > self.max:
            self.current = self.max

    def percent(self):
        return self.current / self.max

    def draw(self, x, y, r):
        pygame.draw.rect(screen, self.border, (x - 30, y - 1.5 * r, 60, 5))
        pygame.draw.rect(screen, self.fill, (x - 30, y - 1.5 * r, 60 * self.percent(), 5))

class Bar:
    def __init__(self, MAX, rect, fill = "green", border = "red"):
        self.max = MAX
        self.current = MAX
        self.fill = fill
        self.border = border
        self.rect = rect
        self.x = WIDTH//2
        self.y = HEIGHT//2
## 0 = x, 1 = y, 2 = width, 3 = height
    def clicked(self):
        if pygame.mouse.get_pos()[0] < self.rect[0]:
            self.x = self.rect[0]
        elif pygame.mouse.get_pos()[0] > self.rect[0] + self.rect[2]:
            self.x = self.rect[0] + self.rect[2]
        else:
            self.x = (pygame.mouse.get_pos()[0] + self.rect[3] / 20) // self.rect[3] / 10 * self.rect[3] / 10
        pygame.draw.rect(screen, NAVY, (self.rect[0] - self.rect[3] // 20, self.y - 5, 710, 60))
        pygame.draw.rect(screen, "white", (100, self.y, self.x - 100, 50))

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
    # pygame.Surface.blit(screen, text_surf, (50, 50, WIDTH//2, HEIGHT//2))
    while running:
        clock.tick(60)
        screen.fill(NAVY)
        pygame.draw.polygon(screen, "black", [(0,0), (0, HEIGHT), (WIDTH, HEIGHT)])
        play.draw()
        if pygame.mouse.get_pressed():
        # self.function()
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_0]:
                return settings()
        pygame.display.flip()

def game():
    running = True
    global player
    global enemies
    player = Player()
    enemies = []
    projectiles = []
    for i in range (40):
        enemies.append(Enemy())

    last_shot_time = 0
    COOLDOWN = 150
    while running:

        clock.tick(60)
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for projectile in projectiles:
            projectile.shoot()
            if collision(projectile.x, projectile.y, projectile.radius):
                projectiles.remove(projectile)
            for enemy in enemies:
                if math.sqrt((projectile.x - enemy.x)**2 + (projectile.y - enemy.y)**2) < enemy.radius + projectile.radius:
                    enemy.health.change_health(-2)
                    projectiles.remove(projectile)
                if math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2) < enemy.radius + player.radius:
                    player.health.change_health(-2)

        for enemy in enemies:
            enemy.draw()
            if enemy.health.current <= 0:
                enemies.remove(enemy)


        current_time = pygame.time.get_ticks()

        if current_time - last_shot_time > COOLDOWN:
            projectiles.append(Projectile())
            last_shot_time = current_time

        player.draw()
        player.health.change_health(0)
        player.keyBinding()
        pygame.display.flip()

def settings():
    running = True
    global volume
    volume = Health(12, "white", NAVY)
    bar = Bar(500, (100, 800, 50, 50))
    volume.health = int(pygame.mixer.music.get_volume() * 12)
    print(volume.current)
    while running:
        clock.tick(60)
        screen.fill("BLACK")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_0]:
                return menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    volume.change_health(-1)
                if event.key == pygame.K_RIGHT:
                    volume.change_health(1)
        bar.clicked()
        volume.draw(WIDTH//2, HEIGHT//2, 0)
        pygame.mixer.music.set_volume(volume.percent())
        pygame.display.flip()
        

clock = pygame.time.Clock()
pygame.mixer.music.play(loops = 4)
    # print(pygame.mixer.music.get_volume())

game()
# settings()

pygame.quit() # closes pygame window once loop ends