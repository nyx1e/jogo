import pygame

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.set_colorkey((color)) # Transparência preta
        image.blit(self.spritesheet, (0, 0), (width * frame, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

#Biblioteca de mágica
magic_data = { 
    'heal': {'strength': 20, 'cost': 10, 'grafico': 'assets/player/magic/heal/H1.png'},
    'flame': {'strength': 5, 'cost': 20, 'grafico': 'assets/player/magic/flame/F.png'},
    'lighting': {'strength': 10, 'cost': 30, 'grafico': 'assets/player/magic/lighting/L.png'}}

#Biblioteca de inimigos
enemies_data = {
    'slime': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'bite', 'speed': 2, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'canines': {'health': 150, 'exp': 110, 'damage': 8, 'attack_type': 'claw', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'boss': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'baba', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400}}