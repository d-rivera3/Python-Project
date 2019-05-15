from Pacman.app_class import *
from Pacman.main import *
from Tetris import *
import pygame

pygame.init()

pygame.mixer.music.load('screen_select.mp3')
pygame.mixer.music.play(-1,0)

def draw_text(words, screen, pos, size, color, font_name, centered=False):
    font = pygame.font.SysFont(font_name, size)
    text = font.render(words, False, color)
    text_size = text.get_size()
    if centered:
        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)

screen = pygame.display.set_mode((640, 480))

screen.fill((0,0,0))

#get and resize images
pacman_img = pygame.image.load('pacman.png')
pacman_img = pygame.transform.scale(pacman_img, (200, 250))
tetris_img = pygame.image.load('tetris.png')
tetris_img = pygame.transform.scale(tetris_img, (200, 250))

#set font and color for font
basicfont = pygame.font.Font('freesansbold.ttf',18)
white = (255,255,255)

#display text for options
pressKeySurf = basicfont.render("Press 'P' to play Pacman", True, white)
screen.blit(pressKeySurf, (100,300))

pressKeySurf = basicfont.render("Press 'T' to play Tetris", True, white)
screen.blit(pressKeySurf, (350,300))

pressKeySurf = basicfont.render("Close window to quit", True, white)
screen.blit(pressKeySurf, (200, 400))


#display images
screen.blit(pacman_img, (100,20))
screen.blit(tetris_img, (350,10))


pygame.display.update()
pacman = False
tetris = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pacman = True
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            tetris = True
            break
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
    if pacman or tetris:
        pygame.mixer.music.stop()
        break

if pacman:
    app = App()
    app.run()
else:
    Tetris.main()
