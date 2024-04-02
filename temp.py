# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH // 2 ,
                SCREEN_HEIGHT// 2 + 143,
            )
        )
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, 800),
                0,
            )
        )
        self.speed = random.randint(15, 20)
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.bottom > SCREEN_HEIGHT// 2 + 146:
            self.kill()


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
player = Player()

enemies = pygame.sprite.Group()
players = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
players.add(player)


# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
            
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    # Fill the screen with black
    screen.fill((0, 0, 0))

    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False


    clock.tick(30)
    # Update the display
    pygame.display.flip()