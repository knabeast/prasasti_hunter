from csv import reader, writer
from settings import tile_size
from os import walk
import pygame

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
			image_scale = pygame.transform.scale(image_surf, (100, 100))
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
				matrix[row_index][col_index] = 99
			elif val == 1:
				matrix[row_index][col_index] = 98
			else:
				matrix[row_index][col_index] = 1
	print(f"matrix: {matrix}")

	return matrix

def create_int_export(matrix):
	copy_matrix = matrix.copy()
	int_export = [list(map(int,i) ) for i in copy_matrix]
	for row_index, row in enumerate(int_export):
		for col_index,val in enumerate(row):
			if val == 99:
				int_export[row_index][col_index] = -1
			elif val == 98:
				int_export[row_index][col_index] = 1
			else:
				int_export[row_index][col_index] = 0

	return int_export

def create_str_export(int_export):
	str_export = []
	for row in int_export:
		string_row = [str(val) for val in row]
		str_export.append(string_row)

	print(f"exported: {str_export}")

	return str_export