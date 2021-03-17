import pygame, sys, random
from pygame.locals import *

class SnakeGame:
        # display:
        clock = pygame.time.Clock()
        fps = 60

        WINDOW_SIZE = (600, 500)

        pygame.init()

        pygame.display.set_caption('Snake')
        screen = pygame.display.set_mode(WINDOW_SIZE)

        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()

        x, y = width//2-10, height//2  # character begin
        shift_x, shift_y = 0, 0        # shift of direction

        # character:
        snake = pygame.Rect(x, y, 25, 25)

        speed = 5
        tail = []
        lenght_snake = 0
        state_snake = False    # If the snake ate one apple, it can grow.
        head = pygame.transform.scale(pygame.image.load(r'images\head.png'), (25, 25))
        nivel = 4     # how fast to grow

        # background:
        bg = pygame.transform.scale(pygame.image.load(r'images\bg.png'), (width, height))


        # apple:
        score = 0
        apple_img = pygame.transform.scale(pygame.image.load('images\\apple.png'), (25, 25))
        apple_img.set_colorkey((255, 255, 255))

        apple = pygame.Rect(0, 0, 25, 25)
        state_apple = True   # whether or not to drop an apple

        # game music:
        pygame.mixer.init()
        pygame.mixer.music.load('images/snake.mp3')
        pygame.mixer.music.play(loops=-1,start=11)   # always play the music.
        
        def print_score(self):
                font = pygame.font.Font(None,30)
                message = font.render('score: '+str(self.score), 1, (0,0,0), (255,255,255))
                self.screen.blit(message,(470,2))

        def game_over(self):
                while True:
                        #self.screen.fill((0,0,0))
                        font = pygame.font.Font(None,100)
                        message = font.render('YOU LOSE', 1, (255,255,255))
                        self.screen.blit(message, (100,100))
                        
                        font2 = pygame.font.Font(None,70)
                        message = font2.render(f'score: {self.score}', 1, (255,255,255))
                        self.screen.blit(message, (150,200))

                        button = pygame.Rect(150,300, 270,70)
                        pygame.draw.rect(self.screen, (255,100,0), button)

                        message = font2.render('Play Again',1,(0,0,0))
                        self.screen.blit(message, (160,310))
                        
                        pygame.display.update()
                        
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1 and button.collidepoint(event.pos):
                                                self.score = 0  # restart properties
                                                self.snake.x = self.x
                                                self.snake.y = self.y
                                                self.shift_x, self.shift_y = 0, 0
                                                self.tail.clear()
                                                self.lenght_snake = 0
                                                self.state_snake = False
                                                self.state_apple = True
                                                self.run_game()

        def run_game(self):
                while (True):
                        self.screen.blit(self.bg, (0,0))

                        self.snake.x += self.shift_x  # advance according the direction
                        self.snake.y += self.shift_y
                        
                        if self.state_snake:
                                self.tail.append([self.snake.x,self.snake.y,25,25])
                                        
                                for part in self.tail[:-1]:
                                        pygame.draw.rect(self.screen, (0,128,0), part)
                                        
                                self.screen.blit(self.head, self.tail[-1][:2])
                        else:
                                self.screen.blit(self.head, [self.snake.x,self.snake.y]) 
                                
                                
                        if random.randint(1,100) == 1 and self.state_apple:
                                self.apple.x, self.apple.y = random.randint(30,520), random.randint(30,450)
                                self.state_apple = False

                        if len(self.tail) > self.lenght_snake*self.nivel and self.state_snake:
                                self.tail.pop(0)

                                
                        if not self.state_apple:
                                self.screen.blit(self.apple_img, (self.apple.x, self.apple.y))

                        while pygame.Rect.colliderect(self.snake, self.apple) and not self.state_apple:
                                self.score += 1
                                self.lenght_snake += 1
                                self.state_snake = True
                                self.state_apple = True
                        
                        self.print_score() # update the score

                        for part in self.tail[:-1]:
                                if [self.snake.x, self.snake.y] == part[:2]:
                                        self.game_over()
                                        
                        if self.snake.x < 20 or self.snake.y < 20 or self.snake.x > self.WINDOW_SIZE[0] - 45 or self.snake.y > self.WINDOW_SIZE[1] - 40:
                                self.game_over()
                        
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == KEYDOWN:
                                        if event.key == K_LEFT:    # Shift of direction according the keys.
                                                self.shift_x = -self.speed
                                                self.shift_y = 0
                                        if event.key == K_RIGHT:
                                                self.shift_x = self.speed
                                                self.shift_y = 0
                                        if event.key == K_UP:
                                                self.shift_y = -self.speed
                                                self.shift_x = 0
                                        if event.key == K_DOWN:
                                                self.shift_y = self.speed
                                                self.shift_x = 0

                        pygame.display.update()
                        self.clock.tick(self.fps)

game = SnakeGame()
game.run_game()
