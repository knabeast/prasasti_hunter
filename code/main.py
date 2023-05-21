import pygame
import sys
from pygame.locals import *
from settings import *
from level import Level
from overworld import Overworld
from support import check_terrain_new, remove_terrain_new
from button import Button

class Game:
    def __init__(self):
        self.max_level = 0
        self.level = None
        self.status_level = 'terrain'
        
        # audio
        self.bg_sound = pygame.mixer.Sound('./audio/bg.mp3')
        self.bg_sound.set_volume(0.3)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        # self.status = 'overworld'
        self.status = 'menu'
        self.bg_sound.play(loops=-1)

    def create_level(self, current_level):
        self.status_level = check_terrain_new(current_level)
        # self.status_level = 'terrain_new'
        self.level = Level(current_level, screen, self.create_overworld, self.status_level)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_menu(self):
        screen.fill('#84e0ea')
        screen.blit(menuBG, (0, 0))
        screen.blit(title_update, (350, -150))
        if button1.draw():
            self.status = 'overworld'
        if button2.draw():
            remove_terrain_new()
            pygame.quit()
            sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                remove_terrain_new()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.status == 'overworld':
                        self.status = 'menu'
                    elif self.status == 'menu':
                        remove_terrain_new()
                        pygame.quit()
                        sys.exit()
                    elif self.status == 'level':
                        self.status = 'overworld'
                elif event.key == pygame.K_SPACE:
                    if self.status == 'menu':
                        self.status = 'overworld'

    def run(self):
        self.handle_events()
        if self.status == 'menu':
            self.create_menu()
        elif self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
image = pygame.image.load('./graphics/overworld/map.png').convert_alpha()
icon = pygame.image.load('./graphics/cursor/pickaxe.png').convert_alpha()
menuBG = pygame.image.load('./graphics/overworld/menu_bg.png').convert_alpha()
title = pygame.image.load('./graphics/overworld/menu_title.png').convert_alpha()
title_update = pygame.transform.scale(title, (600, 600))

gui_font = pygame.font.SysFont('minecraft', 30, bold=True)
button1 = Button('P L A Y', 300, 80, (500, 400), 5, screen, gui_font, '#f7c45b')
button2 = Button('E X I T', 300, 80, (500, 515), 5, screen, gui_font, '#f7c45b')

game = Game()

while True:
    screen.blit(image, (0, 0))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Mining')

    game.run()

    pygame.display.update()
    clock.tick(60)
