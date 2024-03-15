import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


background = pygame.image.load("assets\\background.png")
rocks = ['assets\\rock1.png',
         'assets\\rock2.png',
         'assets\\rock3.png']

player_moves_right = ['assets\\char_move1.png',
                'assets\\char_move2.png',
                'assets\\char_move3.png',
                'assets\\char_move4.png']

player_moves_left = ['assets\\char_move1_right.png',
                'assets\\char_move2_right.png',
                'assets\\char_move3_right.png',
                'assets\\char_move4_right.png']



pygame.init()
clock = pygame.time.Clock()

counter = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets\char_stand2.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH // 2 ,
                SCREEN_HEIGHT// 2 + 143,
            )
        )
        
        # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            global counter
            self.surf = pygame.image.load(player_moves_left[counter])
            counter = (counter + 1) % len(player_moves_left)
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            # global counter
            self.surf = pygame.image.load(player_moves_right[counter])
            counter = (counter + 1) % len(player_moves_right)
            self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(type).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(50, 750),
                0,
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.bottom > SCREEN_HEIGHT// 2 + 146:
            self.kill()
            
            
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 50, SCREEN_WIDTH + 100),
                random.randint(10, 300),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.bottom < 0:
            self.kill()
            

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 800)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True
# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
            
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy(type = random.choice(rocks))
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            # all_sprites.add(new_cloud)
            
    pressed_keys = pygame.key.get_pressed()
    
    player.update(pressed_keys)
    
    enemies.update()
    clouds.update()
    
    # screen.fill((135, 206, 250))
    screen.blit(background,(0,0))
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)
    # Fill the screen with white
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        

        
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False
        
    
    
    pygame.display.flip()
    clock.tick(30)


