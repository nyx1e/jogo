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

class AnimationPlayer:
    def __init__(self):
        self.frames = {
        #magic    
        'heal': import_folder('assets/player/magic/heal/frames'),
        'flame': import_folder('assets/player/magic/flame/flames'),
        'lighting': import_folder('assets/player/magic/lighting/frames'),

        #morte dos monstros
        'slime': import_folder('assets/enemies/mortes/slime'),
        'canines': import_folder('assets/enemies/mortes/canines')}

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.image.get_rect[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()