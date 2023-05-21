import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type, current_level):
		super().__init__()
		self.current_level = current_level
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump' and current_level == 0:
			self.frames = import_folder('./graphics/character/dust_particles/jump')
		elif type == 'jump' and current_level == 1:
			self.frames = import_folder('./graphics/character/dust_particles/jump2')
		elif type == 'jump' and current_level == 2:
			self.frames = import_folder('./graphics/character/dust_particles/jump2')
		elif type == 'jump' and current_level == 3:
			self.frames = import_folder('./graphics/character/dust_particles/jump2')
		elif type == 'jump' and current_level == 4:
			self.frames = import_folder('./graphics/character/dust_particles/jump2')
		if type == 'land' and current_level == 0:
			self.frames = import_folder('./graphics/character/dust_particles/land')
		elif type == 'land' and current_level == 1:
			self.frames = import_folder('./graphics/character/dust_particles/land2')
		elif type == 'land' and current_level == 2:
			self.frames = import_folder('./graphics/character/dust_particles/land2')
		elif type == 'land' and current_level == 3:
			self.frames = import_folder('./graphics/character/dust_particles/land2')
		elif type == 'land' and current_level == 4:
			self.frames = import_folder('./graphics/character/dust_particles/land2')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()