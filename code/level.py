import pygame 
from support import *
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Level:
	def __init__(self, current_level, surface, create_overworld):
		# general setup
		self.cursor = pygame.image.load('./graphics/cursor/selection.png').convert_alpha()
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		# overworld connection
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
		self.matrix = create_matrix(terrain_layout)
		int_matrix = create_int_export(self.matrix)
		str_matrix = create_str_export(int_matrix)
		export_csv_layout(str_matrix, level_data['terrain'])
		self.grid = Grid(matrix = self.matrix)

		# decoration 
		self.sky = Sky(-2)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 20,level_width)
		self.clouds = Clouds(400,level_width,30)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(tile_size,x,y,hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.create_overworld(self.current_level, 0)

	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
			self.create_overworld(self.current_level, self.new_max_level)

	def draw_active_cell(self):
		mouse_pos = pygame.mouse.get_pos()
		row = mouse_pos[1] // 48
		col = mouse_pos[0] // 48
		# print(f"{row}, {col}")
		current_cell_value =  self.matrix[row][col]
		if not current_cell_value == 99:
			rect = pygame.Rect((col * 48, row * 48),(48, 48))
			self.display_surface.blit(self.cursor, rect)

	def create_path(self):
		start_x, start_y = [8, 3]
		start = self.grid.node(start_x, start_y)
		
		mouse_pos = pygame.mouse.get_pos()
		goal_x, goal_y = mouse_pos[0] // 48, mouse_pos[1] // 48
		goal = self.grid.node(goal_x, goal_y)

		finder = AStarFinder()
		self.path,_ = finder.find_path(start, goal, self.grid)
		print('')
		print(self.path)
		print('')

	def update(self):
		self.draw_active_cell()

	def run(self):
		# run the entire game / level 

		# sky 
		self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)

		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		
		# self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)
		
		self.check_death()
		self.check_win()
		self.update()