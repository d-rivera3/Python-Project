import pygame, sys
from settings import *
from player_class import *
from enemy_class import *
pygame.init() #initializes pygame
vec = pygame.math.Vector2 #Holds a position, velocity,



class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, self.p_pos)
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'intro':
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.state == 'reset':
                self.playing_reset()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

#Helper functions
    def draw_text(self, words, screen, pos, size, color, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        #Opening walls file
        #Creating walls list with coordiantes of walls
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
               for xidx, char in enumerate(line):
                   if char == '1':
                       self.walls.append(vec(xidx, yidx))
                   elif char == 'C':
                       self.coins.append(vec(xidx, yidx))
                   elif char == 'P':
                       self.p_pos = vec(xidx,yidx)
                   elif char in ['2', '3', '4', '5']:
                        self.e_pos.append(vec(xidx, yidx))
                   elif char == "B":
                       pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                 self.cell_width, self.cell_height))
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, pos, idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))
        for coin in self.coins:
            pygame.draw.rect(self.background, (167, 179, 34), (coin.x * self.cell_width, coin.y * self.cell_height,
                                                               self.cell_width, self.cell_height))

#Intro functions

    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def intro_update(self):
        pass

    def intro_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR',self.screen, [WIDTH//2, HEIGHT//2 -50],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2 + 50],
                       START_TEXT_SIZE, (44, 167, 198),START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [0,0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()


#Playing functions
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

        #Ghost runs into player
        for enemy in self.enemies:
            if self.player.grid_pos // 2 == enemy.grid_pos // 2:
                self.player.lives -= 1
                self.state = 'reset'

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, WHITE, START_FONT, centered=False)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2 + 60, 0], 18, WHITE, START_FONT )
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def playing_reset(self):
        if self.player.lives < 1:
            self.state = 'playing'
            self.screen.fill(BLACK)
            pygame.display.update()
            print(self.e_pos)
            self.e_pos.clear()
            self.enemies.clear()
            origin = ORIGINAL_E_POS
            print("Original e pos: ", origin)
            for pos in origin:
                self.e_pos.append(pos)
            print(self.e_pos)
            self.make_enemies()
            print(self.enemies)
            pygame.time.delay(100)
            self.run()
        else:
            self.state = 'game_over'
            self.screen.fill(BLACK)
            self.draw_text('GAME OVER', self.screen, [WIDTH // 2, HEIGHT // 2 - 50],
                           START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
            self.intro_events()
            pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE,
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2)), 5)