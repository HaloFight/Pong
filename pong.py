import pygame, sys, random
from enum import Enum

class Block(pygame.sprite.Sprite):
    def __init__ (self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos,speed_x,speed_y,paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_y = 7 *  random.choice((1,-1))
        self.speed_x = 7 *  random.choice((1,-1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self,self.paddles,False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top)< 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1
    
    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time -self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen,bg_color,time_counter_rect)
        screen.blit(time_counter,time_counter_rect)

class Opponent(Block):
    def __init__(self, path, x_pos, y_pos,speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self,ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed * 2
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed * 2
        self.constrain()
        
    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

class GameManager:
    def __init__(self,ball_group,paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.game_state = GameState.MAIN_MENU

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()

                if self.game_state == GameState.MAIN_MENU:
                    if keys[pygame.K_RETURN]:
                        self.game_state = GameState.PLAYING

                elif self.game_state == GameState.PLAYING:       
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            player.movement += player.speed
                        if event.key == pygame.K_UP:
                            player.movement -= player.speed
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player.movement -= player.speed
                        if event.key == pygame.K_UP:
                            player.movement += player.speed

            
            screen.fill(bg_color)
            pygame.draw.rect(screen,accent_color,middle_strip)
            pygame.draw.rect(screen,accent_color,player)
            pygame.draw.rect(screen,accent_color,opponent)
            pygame.draw.ellipse(screen,accent_color,ball)
            pygame.draw.aaline(screen, accent_color, (screen_width/2,0), (screen_width/2,screen_height))

            if self.game_state == GameState.MAIN_MENU:
                menu_text = basic_font.render("Press Enter to Play", True, grey)
                menu_rect = menu_text.get_rect(center=(screen_width / 2, screen_height / 2))
                screen.blit(menu_text, menu_rect)
                
            elif self.game_state == GameState.PLAYING:
                self.paddle_group.draw(screen)
                self.ball_group.draw(screen)

                self.paddle_group.update(self.ball_group)
                self.ball_group.update()
                self.reset_ball()
                self.draw_score()

            if game_manager.player_score == 10 or game_manager.opponent_score == 10:
                self.game_over()

            pygame.display.flip()
            clock.tick(60)

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score),True,accent_color)
        opponent_score = basic_font.render(str(self.opponent_score),True,accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width/2 + 40,screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width/2 - 40,screen_height/2))

        screen.blit(player_score,player_score_rect)
        screen.blit(opponent_score,opponent_score_rect)

    def game_over(self):
        winner_text = ""
        if self.player_score > self.opponent_score:
            winner_text = "Opponent Wins!"
        elif self.player_score < self.opponent_score:
            winner_text = "Player Wins!"

        game_over_text = basic_font.render(winner_text, True, grey)
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))

        restart_text = basic_font.render("Press R to Restart", True, grey)
        restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 20))

        quit_text = basic_font.render("Press Q to Quit", True, grey)
        quit_rect = quit_text.get_rect(center=(screen_width / 2, screen_height / 2 + 80))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.player_score = 0
                        self.opponent_score = 0
                        self.ball_group.sprite.reset_ball()
                        self.game_state = GameState.PLAYING
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
 
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('pong')

bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
grey = (128,128,128)
basic_font = pygame.font.Font("freesansbold.ttf",32)
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width/2 - 2,0,4,screen_height)

opponent = Opponent('paddle.png',screen_width - 20,screen_height/2,5)
player = Player('Paddle.png',20,screen_width/2,5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png',screen_width/2, screen_height/2,4,4,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group)

game_manager.run_game()