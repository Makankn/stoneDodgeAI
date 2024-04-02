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
    QUIT
    
) 

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

pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

counter = 0
top_score = 0
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
        
        self.last_positions = []  # Store last few positions
        self.position_check_interval = 30  # Check position every 30 frames
        self.move_threshold = 10  # Minimum distance to be considered as movement
        
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
            
    def auto_move(self, right = False):
        
        if right:
            self.rect.move_ip(8, 0)
        else:
            self.rect.move_ip(-8, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


            
            
    def update_last_positions(self):
        # Call this method every frame to update the position history
        if len(self.last_positions) >= self.position_check_interval:
            self.last_positions.pop(0)  # Remove the oldest position
        self.last_positions.append(self.rect.center)  # Add the current position

    def has_moved_recently(self):
        # Check if the player has moved significantly in recent frames
        if len(self.last_positions) < self.position_check_interval:
            return True  # Not enough data to determine, assume movement
        initial_position = self.last_positions[0]
        for pos in self.last_positions[1:]:
            if abs(pos[0] - initial_position[0]) > self.move_threshold or abs(pos[1] - initial_position[1]) > self.move_threshold:
                return True  # Significant movement detected
        return False  # No significant movement

            
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(type).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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


pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 450)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 800)


player = Player()

enemies = pygame.sprite.Group()
players = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players.add(player)
all_sprites.add(player)





enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

all_sprites.add(player)



# Variable to keep the main loop running
running = True
player_alive = True


# Main loop
while running:

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False


        elif event.type == QUIT:
            running = False
            
        elif event.type == ADDENEMY:

            new_enemy1 = Enemy(type = random.choice(rocks))
            enemies.add(new_enemy1)
            all_sprites.add(new_enemy1)
            new_enemy2 = Enemy(type = random.choice(rocks))
            enemies.add(new_enemy2)
            all_sprites.add(new_enemy2)
            

        elif event.type == ADDCLOUD:

            new_cloud = Cloud()
            clouds.add(new_cloud)

            
    pressed_keys = pygame.key.get_pressed()
    

    player.update(pressed_keys)

    
    enemies.update()
    clouds.update()
    
    screen.blit(background, (0, 0))
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        


    if player.alive and pygame.sprite.spritecollideany(player, enemies):
            impact_sound.play()
            player.alive = False  
            pygame.display.flip()
            player.kill() 
            if len(players) ==0:
                quit()
            break
        
        

    pygame.display.flip()
 
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
    
