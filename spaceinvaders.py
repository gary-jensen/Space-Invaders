import pygame
import random
from player import Player
from alien import Alien
from laser import Laser
from missile import Missile
from gamestate import GameState
from text import Text

class SpaceInvaders():
    def __init__(self):
        # Initialize the pygame
        pygame.init()
        self.width = 754
        self.height = 600
        self.getTicksLastFrame = 0
        self.is_running = True

        # Create the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.transparent = pygame.Surface([754,600])
        self.transparent.set_alpha(170)
        self.green_left = pygame.Rect(0, 0, 4, 600)
        self.green_right = pygame.Rect(self.width - 4, 0, 4, 600)

        # Title and Icon
        pygame.display.set_caption('Space Invaders')
        icon = pygame.image.load('alien.png')
        pygame.display.set_icon(icon)

        self.game_state = GameState.START
        self.missile_period = 500        

        self.init_game()
    
    def init_game(self):
        # Init Player
        self.player = Player(self.screen, self.width / 2 - 32, 560)
        self.score = 0

        # Font Text
        self.start_text = Text('START', 100, self.width / 2, 150)
        self.start_sub_text = Text('Press any key to start', 30, self.width / 2, 200)
        self.end_text = Text('GAME OVER', 100, self.width / 2, 150)
        self.end_sub_text = Text('Press any key to play again', 30, self.width / 2, 200)
        self.lives_text = Text(f'LIVES {self.player.lives}', 50, 540, 15)
        self.score_text = Text(f'SCORE {self.score}', 50, 20, 15)
        self.big_score_text = Text(f'SCORE: {self.score}', 50, self.width/2, self.height/2)

        self.reset_game()
    
    def reset_game(self):
        # Init Missiles
        self.missiles = []
        self.last_shoot_time = 0
        self.is_shooting = False

        # Init Lasers
        self.lasers = []
        self.laser_last_time = pygame.time.get_ticks()
        self.laser_period = 900

        # Init Aliens
        self.aliens = []
        self.alien_width = 52
        self.alien_max = self.width - 10 * self.alien_width - 42
        self.aliens_pos = self.alien_max / 2
        self.alien_dir = 1
        self.alien_speed = 0.02
        
        for row in range(5):
            for col in range(11):
                alien_x = col * self.alien_width + self.aliens_pos
                alien_y = row * self.alien_width + 80
                alien = Alien(self.screen, alien_x, alien_y, col)
                self.aliens.append(alien)

        # Reset Player
        self.move_left = False
        self.move_right = False
        self.player.setX(self.width / 2 - 32)
        
        # Reset Score
        self.score_text.set_text(f'SCORE {self.score}')
    
    def update(self):
        current_time = pygame.time.get_ticks()
        deltaTime = (current_time - self.getTicksLastFrame)
        self.getTicksLastFrame = current_time

        self.check_events()

        if self.game_state == GameState.START:
            pass # Main menu
        elif self.game_state == GameState.GAME:
            self.update_player(deltaTime)
            self.update_missiles(deltaTime)
            self.update_aliens(deltaTime)
            self.update_lasers(deltaTime)
            self.check_collisions()
        elif self.game_state == GameState.END:
            pass # Game Over
        elif self.game_state == GameState.PAUSE:
            pass # Pause (do last)

    def check_events(self):
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                self.is_running = False
            
            # Keyboard Input
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.START:
                    self.init_game()
                    self.game_state = GameState.GAME
                elif self.game_state == GameState.GAME :
                    # Left Pressed
                    if event.key == pygame.K_a:
                        self.move_left = True
                    # Right Pressed
                    if event.key == pygame.K_d:
                        self.move_right = True
                    # Space Pressed
                    if event.key == pygame.K_SPACE:
                        self.is_shooting = True
                elif self.game_state == GameState.END:
                    self.init_game()
                    self.game_state = GameState.GAME
            if event.type == pygame.KEYUP:
                if self.game_state == GameState.START:
                    pass
                elif self.game_state == GameState.GAME:
                    # Left Released
                    if event.key == pygame.K_a:
                        self.move_left = False
                    # Right Released
                    if event.key == pygame.K_d:
                        self.move_right = False
                    # Space Released
                    if event.key == pygame.K_SPACE:
                        self.is_shooting = False
    
    def update_player(self, deltaTime):
        if self.move_right and not self.move_left:
            self.player.dirX = 1
        elif self.move_left and not self.move_right:
            self.player.dirX = -1
        else:
            self.player.dirX = 0
        
        self.player.update(deltaTime)

        self.lives_text.set_text(f'LIVES {self.player.lives}')
        # Check player lives
        if self.player.lives <= 0:
            # die
            self.game_state = GameState.END

        # Check player bounds
        if self.player.rect.x + self.player.rect.width > self.width - 6:
            self.player.setX(self.width - self.player.rect.width - 6)
        if self.player.rect.x < 6:
            self.player.setX(6)

    def update_missiles(self, deltaTime):
        if self.is_shooting:
            # Time since last shot. For a max fire rate.
            shoot_time = pygame.time.get_ticks()
            time_since_shoot = shoot_time - self.last_shoot_time

            if time_since_shoot > self.missile_period:
                missileX = self.player.rect.x + (self.player.rect.width / 2)
                missileY = self.player.rect.y + 15
                self.missiles.append(Missile(self.screen, missileX, missileY))
                # Reset last shoot time
                self.last_shoot_time = shoot_time
            
        for missile in self.missiles:
            # update missile pos
            missile.update(deltaTime)
            if missile.lives <= 0 or missile.posY < -100:
                self.missiles.remove(missile)

    def update_aliens(self, deltaTime):
        if len(self.aliens) > 0:
            jump = False
            if self.aliens_pos >= self.alien_max:
                self.alien_dir = -1
                jump = True
            elif self.aliens_pos <= 10:
                self.alien_dir = 1
                jump = True

            if jump == True:
                # increase speed and decrease laser_period
                self.alien_speed += 0.004
                self.laser_period -= 10
                
            self.aliens_pos += self.alien_dir * self.alien_speed * deltaTime
            for alien in self.aliens:
                alien.posX = self.aliens_pos + alien.col * self.alien_width
                alien.update(deltaTime)
                if jump == True:
                    alien.jump()
                if alien.lives <= 0:
                    self.aliens.remove(alien)
            if len(self.aliens) > 0:
                if self.aliens[-1].posY >= 440: # or 400
                    self.player.lives = 0
            
        else:
            # If all aliens dead, reset
            self.reset_game()

    def update_lasers(self, deltaTime):
        shoot_time = pygame.time.get_ticks()
        time_since_shoot = shoot_time - self.laser_last_time

        if time_since_shoot > self.laser_period and len(self.aliens) > 0:
            # create laser
            rand = random.randrange(len(self.aliens))
            x = self.aliens[rand].rect.x
            y = self.aliens[rand].rect.y
            laser = Laser(self.screen, x, y)
            self.lasers.append(laser)
            self.laser_last_time = shoot_time
        
        for laser in self.lasers:
            laser.update(deltaTime)
            if laser.lives <= 0 or laser.posY > self.width:
                self.lasers.remove(laser)

    def check_collisions(self):
        for missile in self.missiles:
            for alien in self.aliens:
                if missile.collide(alien):
                    self.score += 1
                    self.score_text.set_text(f'SCORE {self.score}')
            for laser in self.lasers:
                missile.collide(laser)
        for laser in self.lasers:
            laser.collide(self.player)
        
    def draw(self):
        # Update Background
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), self.green_left)
        pygame.draw.rect(self.screen, (0, 255, 0), self.green_right)
        if self.game_state == GameState.START:
            self.start_text.draw_center(self.screen)
            self.start_sub_text.draw_center(self.screen)
        elif self.game_state == GameState.GAME or self.game_state == GameState.END:
            # Draw Lives Text
            self.lives_text.draw_left(self.screen)
            self.score_text.draw_left(self.screen)

            # Draw Missiles
            for missile in self.missiles:
                missile.draw()
            # Draw Aliens
            for alien in self.aliens:
                alien.draw()
            
            for laser in self.lasers:
                laser.draw()

            # Draw Player
            self.player.draw()
            
            if self.game_state == GameState.END:
                self.screen.blit(self.transparent, (0, 0))
                self.end_text.draw_center(self.screen)
                self.end_sub_text.draw_center(self.screen)
                self.big_score_text.set_text(f'SCORE: {self.score}')
                self.big_score_text.draw_center(self.screen)

        # Update Display
        pygame.display.flip()


# Game Loop
game = SpaceInvaders()
while game.is_running:
    game.update()
    game.draw()