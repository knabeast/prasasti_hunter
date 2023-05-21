import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from support import check_terrain_new, remove_terrain_new

class Game:
    def __init__(self):
        self.max_level = 0
        self.level = None
        self.status_level = 'terrain'
        
        # audio
        self.bg_sound = pygame.mixer.Sound('./audio/bg.wav')
        self.bg_sound.set_volume(0.2)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.waiting_left = None
        self.waiting_right = None
        self.waiting_middle = None
        self.attack_duration = 700
        self.row = None
        self.col = None
        self.bg_sound.play(loops= -1)

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

    def check_mouse_left_click(self):
        if pygame.mouse.get_pressed()[0] and self.status == 'level':
            self.row, self.col = self.level.get_active_cell()
            self.waiting_left = pygame.time.get_ticks() + self.attack_duration

        if self.waiting_left and pygame.time.get_ticks() >= self.waiting_left:
            self.level.remove_level_cell(self.row, self.col)
            self.waiting_left = None
    
    def check_mouse_right_click(self):
        if pygame.mouse.get_pressed()[2] and self.status == 'level':
            self.row, self.col = self.level.get_active_cell()
            self.waiting_right = pygame.time.get_ticks() + self.attack_duration

        if self.waiting_right and pygame.time.get_ticks() >= self.waiting_right:
            self.level.add_level_cell(self.row, self.col)
            self.waiting_right = None
            
            self.level.hint_click()
    
    def check_mouse_middle_click(self):
        if pygame.mouse.get_pressed()[1] and self.status == 'level':
            self.level.hint_click()
            self.waiting_middle = pygame.time.get_ticks() + self.attack_duration

        if self.waiting_middle and pygame.time.get_ticks() >= self.waiting_middle:
            self.level.empty_path()
            self.level.hint_end()
            self.waiting_middle = None

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
image = pygame.image.load('./graphics/overworld/map.png').convert_alpha()
icon = pygame.image.load('./graphics/cursor/pickaxe.png').convert_alpha()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            remove_terrain_new()
            pygame.quit()
            sys.exit()

    screen.blit(image, (0, 0))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Mining')
    game.check_mouse_left_click()
    game.check_mouse_right_click()
    game.check_mouse_middle_click()
    game.run()

    pygame.display.update()
    clock.tick(60)
