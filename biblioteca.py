import pygame
from os import walk

def import_folder(path):
    surf_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)
    return surf_list

#Biblioteca de mágica
magic_data = { 
    'heal': {'strength': 20, 'cost': 10, 'grafico': 'assets/player/magic/H1.png'},
    'flame': {'strength': 25, 'cost': 20, 'grafico': 'assets/player/magic/F.png'},
    'raio': {'strength': 35, 'cost': 30, 'grafico': 'assets/player/magic/L.png'}}

#Biblioteca de inimigos
enemies_data = {
    'slime': {'health': 80, 'exp': 100, 'damage': 5, 'attack_type': 'bite', 'speed': 1, 'resistance': 4, 'attack_radius': 60, 'notice_radius': 300},
    'canines': {'health': 100, 'exp': 110, 'damage': 15, 'attack_type': 'claw', 'speed': 3, 'resistance': 4, 'attack_radius': 80, 'notice_radius': 360},
    'boss': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'baba', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400}}

#vida 80/100/300