import pygame, sys

class Button:
	def __init__(self,text,width,height,pos,elevation,surface,font, text_color):
		#Core attributes 
		self.text_color = text_color
		self.text = text
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		self.display_surface = surface
		self.button_font = font

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		# self.top_color = '#ef5f62'
		self.top_color = '#f7c45b'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		# self.bottom_color = '#c93a56'
		self.bottom_color = '#312d44'
		#text
		self.text_surf = self.button_font.render(text,True, self.text_color)
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(self.display_surface,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(self.display_surface,self.top_color, self.top_rect,border_radius = 12)
		self.display_surface.blit(self.text_surf, self.text_rect)
		
		return self.check_click()

	def check_click(self):
		action = False
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#ef5f62'
			self.text_color = '#f7c45b'
			self.text_surf = self.button_font.render(self.text,True, self.text_color)
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					action = True
					self.pressed = False
		else:
			self.top_color = '#f7c45b'
			self.text_color = '#ef5f62'
			self.dynamic_elecation = self.elevation
			self.text_surf = self.button_font.render(self.text,True, self.text_color)
		
		return action
        