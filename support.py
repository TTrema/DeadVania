import pygame, os, json
from settings import *
from csv import reader

def import_folder(path):
    surface_list = []

    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            size = 64
            if 'sheet' in full_path:
                if 'boar' in full_path:
                    size = 32
                image_surf2 = import_cut_graphics(full_path, size)  
                for image in image_surf2:
                    surface_list.append(image) 
            else:       
                surface_list.append(image_surf)


    return surface_list

def import_folder_dict(path):
	surface_dict = {}

	for folder_name, sub_folders, img_files in os.walk(path):
		for image_name in img_files:
			full_path = path + '/' + image_name
			image_surf = pygame.image.load(full_path)
			surface_dict[image_name.split('.')[0]] = image_surf
			
	return surface_dict

def import_cut_graphics(path, size):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / size)
    tile_num_y = int(surface.get_size()[1] / size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size
            y = row * size
            new_surf = pygame.Surface((size, size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size, size))
            cut_tiles.append(new_surf)

    return cut_tiles

def import_cut_graphics_size(path, size):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surf)

    return cut_tiles



def import_csv_layout(path):

    terrain_map = []    
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def load_existing_save(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        controls = json.load(file)
    return controls

def write_save(data):
    with open(os.path.join(os.getcwd(),'save.json'), 'w') as file:
        json.dump(data, file)
        
def write_joy_save(data):
    with open(os.path.join(os.getcwd(),'joy.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    print('1')
    try:
    # Save is loaded 
        joy_save = load_existing_save('joy.json')
        save = load_existing_save('save.json')
    except:
    # No save file, so create one
        joy_save = create_joy_save()
        write_joy_save(joy_save)
        save = create_save()
        write_save(save)
    return save, joy_save



def create_save():
    new_save = {
    "controls":{
        "0" :{"Left": pygame.K_LEFT, "Right": pygame.K_RIGHT, "Up": pygame.K_UP, "Down": pygame.K_DOWN, 
            "Jump": pygame.K_SPACE, "Attack": pygame.K_a,"Magic": pygame.K_s, 
            "Dodge": pygame.K_LSHIFT, "Start": pygame.K_RETURN, "Select": pygame.K_m},
        "1" :{"Left": pygame.K_LEFT, "Right": pygame.K_RIGHT, "Up": pygame.K_UP, "Down": pygame.K_DOWN, 
            "Jump": pygame.K_SPACE, "Attack": pygame.K_a,"Magic": pygame.K_s, 
            "Dodge": pygame.K_LSHIFT, "Start": pygame.K_RETURN, "Select": pygame.K_m}
        },
    "current_profile": 0
    }

    return new_save

def create_joy_save():
    new_save = {"joy": {"Jump": 0, "Attack": 2, "Magic": 3, "Dodge": 4, "Start": 7, "Select": 6}}
    return new_save
    

def reset_keys(actions):
    for action in actions:
        actions[action] = False
    return actions