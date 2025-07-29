import pygame
from biblioteca import import_folder

class AnimationPlayer:
    def __init__(self):
        self.frames = {
        #magic    
        'heal': import_folder('assets/player/magic/heal'),
        'flame': import_folder('assets/player/magic/flame'),
        'horizontal': import_folder('assets/player/magic/raio/horizontal'), 
        'vertical': import_folder('assets/player/magic/raio/vertical'),

        #morte dos monstros
        'slime': import_folder('assets/enemies/mortes/slime'),
        'canines': import_folder('assets/enemies/mortes/canines')}

    def create_particles(self,animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
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