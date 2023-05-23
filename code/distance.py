import pygame
from settings import *

class Distance:
    def __init__(self, surface):
        self.display_surface = surface
        self.font = pygame.font.SysFont('minecraft', 30, bold=True)
        self.distance_rect = pygame.Rect((screen_width/2 - 96, screen_height - 32), (30, 30))

    def show_distance(self, num):
        distance_surf = self.font.render(f"Distance: {str(num)}", False, '#E6E6E6')
        self.display_surface.blit(distance_surf, self.distance_rect)