import pygame, sys
from settings import * 
from level import Level
from game_data import level_0
from overworld import Overworld

class Game:
	def __init__(self):
		self.max_level = 5
		self.level = None

		# overworld creation
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld)
		self.status = 'level'

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'

	def handle_mouse_click(self):
		if pygame.mouse.get_pressed()[0]:
			if self.status == 'level':
				self.level.create_path()

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()

# Pygame setupd
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
image = pygame.image.load('./graphics/overworld/map.png').convert_alpha()
game = Game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.blit(image, (0, 0))
	# screen.fill('#703f56')
	game.handle_mouse_click() 
	game.run()

	pygame.display.update()
	clock.tick(60)
	