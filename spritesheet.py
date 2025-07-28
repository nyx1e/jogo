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
    'heal': {'strength': 20, 'cost': 10, 'grafico': 'animação'},
    'flame': {'strength': 5, 'cost': 20, 'grafico': 'animação'}}