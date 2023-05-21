import pygame
from csv import reader, writer
from settings import tile_size
from os import walk, remove, path

def import_folder(path):
	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_folder_2(path):
	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			image_scale = pygame.transform.scale(image_surf, (250, 250))
			surface_list.append(image_scale)

	return surface_list

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map
	
def export_csv_layout(terrain_map, path):
    with open(path, mode='w', newline='') as map:
        level = writer(map, delimiter=',')
        level.writerows(terrain_map)

def import_cut_graphics(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_size)
	tile_num_y = int(surface.get_size()[1] / tile_size)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
			cut_tiles.append(new_surf)

	return cut_tiles

def create_matrix(terrain_layout):
	copy_terrain_layout = terrain_layout.copy()
	matrix = [list(map(int,i) ) for i in copy_terrain_layout]
	for row_index, row in enumerate(matrix):
		for col_index,val in enumerate(row):
			if val == -1:
				matrix[row_index][col_index] = 1
			elif val == 0:
				matrix[row_index][col_index] = 2
			elif val == 6:
				matrix[row_index][col_index] = 2
			elif val == 1:
				matrix[row_index][col_index] = 3
			elif val == 4:
				matrix[row_index][col_index] = 3
			elif val == 7:
				matrix[row_index][col_index] = 3
			elif val == 2:
				matrix[row_index][col_index] = 0
			elif val == 5:
				matrix[row_index][col_index] = 0
			elif val == 8:
				matrix[row_index][col_index] = 0

	# print(f"{matrix}\n")
	return matrix

def create_int_export(matrix, current_level):
	copy_matrix = matrix.copy()
	int_export = [list(map(int,i) ) for i in copy_matrix]
	for row_index, row in enumerate(int_export):
		for col_index,val in enumerate(row):
			if current_level == 0:
				if val == 1:
					int_export[row_index][col_index] = -1
				elif val == 2:
					int_export[row_index][col_index] = 0
				elif val == 3:
					int_export[row_index][col_index] = 1
				elif val == 0:
					int_export[row_index][col_index] = 2
			elif current_level == 1:
				if val == 1:
					int_export[row_index][col_index] = -1
				elif val == 3:
					int_export[row_index][col_index] = 4
				elif val == 0:
					int_export[row_index][col_index] = 5
			elif current_level == 2:
				if val == 1:
					int_export[row_index][col_index] = -1
				elif val == 2:
					int_export[row_index][col_index] = 6
				elif val == 3:
					int_export[row_index][col_index] = 7
				elif val == 0:
					int_export[row_index][col_index] = 8
			elif current_level == 3:
				if val == 1:
					int_export[row_index][col_index] = -1
				elif val == 3:
					int_export[row_index][col_index] = 4
				elif val == 0:
					int_export[row_index][col_index] = 5
			elif current_level == 4:
				if val == 1:
					int_export[row_index][col_index] = -1
				elif val == 2:
					int_export[row_index][col_index] = 6
				elif val == 3:
					int_export[row_index][col_index] = 7
				elif val == 0:
					int_export[row_index][col_index] = 8

	# print(f"{int_export}")
	return int_export

def create_str_export(int_export):
	str_export = []
	for row in int_export:
		string_row = [str(val) for val in row]
		str_export.append(string_row)

	return str_export

def create_matrix_player(player_layout):
	copy_player_layout = player_layout.copy()
	matrix_player = [list(map(int,i) ) for i in copy_player_layout]
	for row_index, row in enumerate(matrix_player):
		for col_index,val in enumerate(row):
			if val == -1:
				matrix_player[row_index][col_index] = 2
			elif val == 1:
				matrix_player[row_index][col_index] = 1
			else:
				matrix_player[row_index][col_index] = 0

	return matrix_player

def get_row_col_matrix_player(matrix_player):
	for row_index, row in enumerate(matrix_player):
		for col_index,val in enumerate(row):
			if val == 1:
				return row_index, col_index

def remove_terrain_new():
	csv_files =	[
		"./levels/0/level_0_terrain_new.csv", 
		"./levels/1/level_1_terrain_new.csv", 
		"./levels/2/level_2_terrain_new.csv", 
		"./levels/3/level_3_terrain_new.csv", 
		"./levels/4/level_4_terrain_new.csv"]
	total_files = len(csv_files)
	for i in range(total_files):
		if(path.exists(csv_files[i])):
			remove(csv_files[i])
			# print(f"{csv_files[i]} found")
		else:
			pass

def check_terrain_new(current_level):
	csv_file = f"./levels/{current_level}/level_{current_level}_terrain_new.csv"
	if(path.exists(csv_file)):
		status_level = 'terrain_new'
	else:
		status_level = 'terrain'
	return status_level
