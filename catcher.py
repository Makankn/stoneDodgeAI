import pygame
import random
import time
import numpy
import neat
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
# random.seed(43)
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
my_font = pygame.font.SysFont('Times New Roman', 30)

clock = pygame.time.Clock()

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
    # def update(self, pressed_keys):
        
    #     if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
    #         self.surf = pygame.image.load("assets\char_stand2.png").convert_alpha()
    #     # if pressed_keys[K_UP]:
    #     #     self.rect.move_ip(0, -5)
    #     # if pressed_keys[K_DOWN]:
    #     #     self.rect.move_ip(0, 5)
    #     if pressed_keys[K_LEFT]:
    #         global counter
    #         self.surf = pygame.image.load(player_moves_left[counter])
    #         counter = (counter + 1) % len(player_moves_left)
    #         self.rect.move_ip(-5, 0)
    #     if pressed_keys[K_RIGHT]:
    #         # global counter
    #         self.surf = pygame.image.load(player_moves_right[counter])
    #         counter = (counter + 1) % len(player_moves_right)
    #         self.rect.move_ip(5, 0)
    #     # Keep player on the screen
    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #     if self.rect.right > SCREEN_WIDTH:
    #         self.rect.right = SCREEN_WIDTH
    #     if self.rect.top <= 0:
    #         self.rect.top = 0
    #     if self.rect.bottom >= SCREEN_HEIGHT:
    #         self.rect.bottom = SCREEN_HEIGHT
            
    def auto_move(self, right = False):
        
        if right:
            global counter
            
            self.surf = pygame.image.load(player_moves_right[counter])
            counter = (counter + 1) % len(player_moves_right)
            self.rect.move_ip(8, 0)
        else:
            
            self.surf = pygame.image.load(player_moves_left[counter])
            counter = (counter + 1) % len(player_moves_left)
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
            
class Side_Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Side_Enemy, self).__init__()
        self.surf = pygame.image.load(type).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.choice([0,800]),
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
            
# def get_game_state(player, enemies):
#     # Normalize player position
#     player_pos = (player.rect.x / SCREEN_WIDTH, player.rect.y / SCREEN_HEIGHT)
    
#     # Initialize closest and second closest enemies
#     closest_enemy_distance = float('inf')
#     second_closest_enemy_distance = float('inf')
#     closest_enemy_position = (0, 0)
#     second_closest_enemy_position = (0, 0)

#     for enemy in enemies:
#         distance = ((player.rect.x - enemy.rect.x) ** 2 + (player.rect.y - enemy.rect.y) ** 2) ** 0.5
#         if distance < closest_enemy_distance:
#             # Update second closest with previous closest
#             second_closest_enemy_distance = closest_enemy_distance
#             second_closest_enemy_position = closest_enemy_position
#             # Update closest
#             closest_enemy_distance = distance
#             closest_enemy_position = (enemy.rect.x / SCREEN_WIDTH, enemy.rect.y / SCREEN_HEIGHT)
#         elif distance < second_closest_enemy_distance:
#             # Update second closest
#             second_closest_enemy_distance = distance
#             second_closest_enemy_position = (enemy.rect.x / SCREEN_WIDTH, enemy.rect.y / SCREEN_HEIGHT)

#     # Normalize distances
#     closest_enemy_distance_normalized = closest_enemy_distance / (SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) ** 0.5
#     second_closest_enemy_distance_normalized = second_closest_enemy_distance / (SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) ** 0.5

#     # Construct the game state
#     game_state = [
#         closest_enemy_position[0],closest_enemy_position[1],  # Closest enemy X, Y
#         closest_enemy_distance_normalized,  # Normalized distance to closest enemy
#         second_closest_enemy_position[0], second_closest_enemy_position[1], # Second closest enemy X, Y
#         second_closest_enemy_distance_normalized  # Normalized distance to second closest enemy
#     ]

#     return game_state

def get_game_state(player, enemies):
    player_pos = (player.rect.x / SCREEN_WIDTH, player.rect.y / SCREEN_HEIGHT)

    # Player movement state (1 for right, -1 for left, 0 for still)
    player_movement = 0  # Default to still
    player_x , player_y = player.rect.center
    if player.last_positions:  # Check if there are any recorded positions
        if player.rect.center == player.last_positions[-1]:
            player_movement = 0
        elif player.rect.center[0] > player.last_positions[-1][0]:
            player_movement = 1
        elif player.rect.center[0] < player.last_positions[-1][0]:
            player_movement = -1

    # Number of enemies on screen
    enemy_count = len(enemies)

    # Player's distance from screen edges
    distance_from_left_edge = player.rect.x / SCREEN_WIDTH
    distance_from_right_edge = (SCREEN_WIDTH - player.rect.x) / SCREEN_WIDTH

    # Initialize closest and second closest enemies
    closest_enemy_distance = float('inf')
    second_closest_enemy_distance = float('inf')
    closest_enemy_speed = 0  # Speed of the closest enemy
    second_closest_enemy_speed = 0  # Speed of the closest enemy
    
    closest_enemy_position = (0, 0)
    second_closest_enemy_position = (0, 0)

    for enemy in enemies:
        distance = ((player.rect.x - enemy.rect.x) ** 2 + (player.rect.y - enemy.rect.y) ** 2) ** 0.5
        if distance < closest_enemy_distance:
            # Update second closest with previous closest
            second_closest_enemy_distance = closest_enemy_distance
            second_closest_enemy_position = closest_enemy_position
            # Update closest
            closest_enemy_distance = distance
            closest_enemy_speed = enemy.speed
            closest_enemy_position = (enemy.rect.x / SCREEN_WIDTH, enemy.rect.y / SCREEN_HEIGHT)
        elif distance < second_closest_enemy_distance:
            # Update second closest
            second_closest_enemy_distance = distance
            second_closest_enemy_speed = enemy.speed
            second_closest_enemy_position = (enemy.rect.x / SCREEN_WIDTH, enemy.rect.y / SCREEN_HEIGHT)

    # Normalize distances
    closest_enemy_distance_normalized = closest_enemy_distance / (SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) ** 0.5
    second_closest_enemy_distance_normalized = second_closest_enemy_distance / (SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) ** 0.5

    # Construct the game state
    game_state = [
        player_movement,  # Player movement state
        distance_from_left_edge,  # Player's distance from left edge
        distance_from_right_edge,  # Player's distance from right edge
        closest_enemy_position[0], closest_enemy_position[1],  # Closest enemy X, Y
        closest_enemy_distance_normalized,  # Normalized distance to closest enemy
        closest_enemy_speed / 20.0,  # Normalized speed of the closest enemy (assuming max speed is 20)

    ]

    return game_state

    return game_state



# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 450)
ADDENEMY_side = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY_side, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 800)

# # player = Player()

# players_list = [Player() for _ in range(10) ]


# enemies = pygame.sprite.Group()
# clouds = pygame.sprite.Group()
# all_sprites = pygame.sprite.Group()
# players = pygame.sprite.Group()

# # all_sprites.add(player)
# players.add(players_list)

# [all_sprites.add(player) for player in players_list]
# # Variable to keep the main loop running
# running = True
# player_alive = True


# # Main loop
# while running:
#     # Look at every event in the queue
#     for event in pygame.event.get():
#         # Did the user hit a key?
#         if event.type == KEYDOWN:
#             # Was it the Escape key? If so, stop the loop.
#             if event.key == K_ESCAPE:
#                 running = False

#         # Did the user click the window close button? If so, stop the loop.
#         elif event.type == QUIT:
#             running = False
            
#         # Add a new enemy?
#         elif event.type == ADDENEMY:
#             # Create the new enemy and add it to sprite groups
#             new_enemy1 = Enemy(type = random.choice(rocks))
#             enemies.add(new_enemy1)
#             all_sprites.add(new_enemy1)
#             new_enemy2 = Enemy(type = random.choice(rocks))
#             enemies.add(new_enemy2)
#             all_sprites.add(new_enemy2)
            
#         # Add a new cloud?
#         elif event.type == ADDCLOUD:
#             # Create the new cloud and add it to sprite groups
#             new_cloud = Cloud()
#             clouds.add(new_cloud)
#             # all_sprites.add(new_cloud)
            
#     pressed_keys = pygame.key.get_pressed()
    
#     for player in players:
#         if player.alive:  # Only update player if alive
#             player.update(pressed_keys)
#             player.auto_move()
    
#     enemies.update()
#     clouds.update()
    
#     screen.blit(background, (0, 0))
#     for entity in clouds:
#         screen.blit(entity.surf, entity.rect)

#     for entity in all_sprites:
#         screen.blit(entity.surf, entity.rect)
        
#     scoretext = my_font.render("Score = "+str(top_score), 1, (0,0,0))
#     screen.blit(scoretext, (5, 10))    
        
#     for player in players:
        
#     # Check for collision only if the player is alive
#         if player.alive and pygame.sprite.spritecollideany(player, enemies):
#             impact_sound.play()
#             player.alive = False  # Mark the player as dead
#             pygame.display.flip()
#             player.kill() # Update the display to show the dead player
#             if len(players) ==0:
#                 quit()
#             break
        
        

#     pygame.display.flip()
#     [x.score_calc() for x in players]
#     top_score = max([x.score for x in players])    
#     clock.tick(30)

# pygame.mixer.music.stop()
# pygame.mixer.quit()


gen = 0

def eval_genomes(genomes, config):
    scores = []
    global gen
    gen +=1 
    global all_sprites, players, enemies, clouds

    # Reset game state for a new generation
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    nets = []
    ge = []
    player_nets = {}
    ge_players = {}
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        player = Player()  # Your Player class instance
        players.add(player)
        all_sprites.add(player)
        player_nets[player] = net  # Map player to its network
        genome.fitness = 0  # Initialize fitness
        # ge.append(genome)
        ge_players[player] = genome

    # Main game loop
    running = True
    while len(players) > 0:
        # print(len(players))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy1 = Enemy(type = random.choice(rocks))
                enemies.add(new_enemy1)
                all_sprites.add(new_enemy1)
                new_enemy2 = Enemy(type = random.choice(rocks))
                enemies.add(new_enemy2)
                all_sprites.add(new_enemy2)
                
            elif event.type == ADDENEMY_side:
                # Create the new enemy and add it to sprite groups
                new_enemy1 = Side_Enemy(type = random.choice(rocks))
                enemies.add(new_enemy1)
                all_sprites.add(new_enemy1)

                
            # Add a new cloud?
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)

        # Update game state and render all entities
        # Assume get_game_state() is a function you define to get inputs for the neural network
        

        for x, player in enumerate(players):
            game_state = get_game_state(player, enemies)
            ge_players[player].fitness += 0.1  # Reward staying alive
            output = player_nets[player].activate(game_state)

            # Decide movement based on neural network output
            # For simplicity, assuming 2 outputs for left and right movement
            
            if output.index(max(output)) == 0:
                player.auto_move(right=True)
            elif output.index(max(output)) == 1:
                player.auto_move()
            # if output[0] > 0.5: player.auto_move(right=True)
            # if output[1] > 0.5: player.auto_move()

            # Update player and check for game over conditions
            # player.update()
        
        # Check for collision only if the player is alive
            if player.alive and pygame.sprite.spritecollideany(player, enemies):
                # impact_sound.play()
                del player_nets[player]
                ge_players[player].fitness -= 1
                player.alive = False
                player.kill()
                pygame.display.flip()
                # ge[x].fitness -= 1  # Penalty for dying
# Update the display to show the dead player
            if player.alive:
                scores.append(ge_players[player].fitness)


        player.update_last_positions()
        if not player.has_moved_recently():
            ge_players[player].fitness -= 0.1

        # Update and draw all game entities

        enemies.update()
        clouds.update()
        avgscore_text_each_generation = my_font.render(f'Avg Score: {int(numpy.average(scores))}', False, (0, 0, 0))
        gen_number = my_font.render(f'generation: {gen}', False, (0, 0, 0))
        
        screen.blit(background, (0, 0))
        
        
        
        
        for entity in clouds:
            screen.blit(entity.surf, entity.rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            
        screen.blit(gen_number, (5,0)) 
        screen.blit(avgscore_text_each_generation, (5,30))
        pygame.draw.rect(screen, ("#76442e"), pygame.Rect(0, 0, 180, 70), 2)
        
        pygame.display.flip()
        clock.tick(30)

# Setup NEAT and run
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward.txt')
p = neat.Population(config)
neat.Checkpointer(20)
p.add_reporter(neat.StdOutReporter(True))
p.add_reporter(neat.StatisticsReporter())

winner = p.run(eval_genomes, 200)  # Run for 50 generations