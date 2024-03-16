import pygame
import random
import time
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
random.seed(43)
pygame.mixer.init()
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


rock_impact_sound = [pygame.mixer.Sound('assets\sound\stone_one.wav'), 
                    pygame.mixer.Sound('assets\sound\stone_two.wav'), 
                    pygame.mixer.Sound('assets\sound\stone_three.wav')]

impact_sound = pygame.mixer.Sound('assets\sound\impact.wav')


pygame.init()
clock = pygame.time.Clock()

counter = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets\char_stand2.png").convert_alpha()
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH // 2 ,
                SCREEN_HEIGHT// 2 + 143,
            )
        )
    
        self.alive = True
        self.sec_counter = 0
        self.score = 0
        self.moves = ['right', 'left']
        
    def score_calc(self):
        self.sec_counter+=1
        if self.sec_counter %150 ==0:
            self.sec_counter=0
            self.score +=1
            
        
        # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        
        if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("assets\char_stand2.png").convert_alpha()
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
            
    def auto_move(self):
        move = random.choice(self.moves)
        if move == 'right':
            self.rect.move_ip(5, 0)
        else:
            self.rect.move_ip(-5, 0)
            
        

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
        self.speed = random.randint(10, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.bottom > SCREEN_HEIGHT// 2 + 146:
            random.choice(rock_impact_sound).play(fade_ms=100)
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
pygame.time.set_timer(ADDENEMY, 450)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 800)

# player = Player()

players_list = [Player() for _ in range(10) ]


enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

# all_sprites.add(player)
players.add(players_list)

[all_sprites.add(player) for player in players_list]
# Variable to keep the main loop running
running = True
player_alive = True

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
            new_enemy1 = Enemy(type = random.choice(rocks))
            enemies.add(new_enemy1)
            all_sprites.add(new_enemy1)
            new_enemy2 = Enemy(type = random.choice(rocks))
            enemies.add(new_enemy2)
            all_sprites.add(new_enemy2)
            
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            # all_sprites.add(new_cloud)
            
    pressed_keys = pygame.key.get_pressed()
    
    for player in players:
        if player.alive:  # Only update player if alive
            player.update(pressed_keys)
            player.auto_move()
    
    enemies.update()
    clouds.update()
    
    screen.blit(background, (0, 0))
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    for player in players:
    # Check for collision only if the player is alive
        if player.alive and pygame.sprite.spritecollideany(player, enemies):
            impact_sound.play()
            player.alive = False  # Mark the player as dead
            pygame.display.flip()
            player.kill() # Update the display to show the dead player
            # time.sleep(2)
            # Wait for 2 seconds to show the dead animation
            if len(players) ==0:
                quit()
            break
        
        

    pygame.display.flip()
        
    player.score_calc()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()

