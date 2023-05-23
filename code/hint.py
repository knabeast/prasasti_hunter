import pygame
from settings import *

class Hint:
    def __init__(self, click_bool):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()
        self.click_bool = click_bool

    def create_buttons(self):
        size = 48
        margin = 24
        topleft = (screen_width/2 + 36, screen_height - size)
        # topleft = (screen_width/2 - size/2 - margin/2, size/2 + margin/2)
        # topleft = (screen_width - size - margin, size/2 + margin/2)
        self.rect = pygame.Rect(topleft, (size, size))

        # button area
        button_margin = 12
        button_rect = pygame.Rect(self.rect.topleft, (size, size))
        self.hint_button_rect = button_rect.copy().inflate(-button_margin, -button_margin)

        # hint button
        self.hint_button = pygame.sprite.GroupSingle()
        Button(self.hint_button_rect, self.hint_button)

    def highlight(self):
        pygame.draw.rect(self.display_surface, '#E6E6E6', self.hint_button_rect.inflate(4, 4), 5, 4)

    def broder(self):
        pygame.draw.rect(self.display_surface, '#807F8A', self.hint_button_rect.inflate(4, 4), 5, 4)

    def display(self):
        self.hint_button.update()
        self.hint_button.draw(self.display_surface)
        self.broder()
        if self.click_bool:
            self.highlight()

class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect
        self.item = pygame.image.load('./graphics/cursor/hint.png').convert_alpha()

    def update(self):
        self.image.fill('#33323d')
        hint = self.item
        rect = self.item.get_rect(center=(self.rect.width/2, self.rect.height/2))
        self.image.blit(hint, rect)