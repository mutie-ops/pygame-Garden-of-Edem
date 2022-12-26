from settings import *
import pygame
from support import import_folder


class AnimationPlayer:
    def __init__(self):
        # MAGIC PARTICLES
        self.frames = {'die': import_folder('/tiles/powers/die'),
                       'flame': import_folder('/tiles/powers/flame'),
                       'heal': import_folder('/tiles/powers/heal'),

                       # MONSTER DEATHS
                       'goblin_general': import_folder('/tiles/enemy/die'),

                       # MONSTER ATTACK
                       'slash': import_folder('/tiles/slash_fx')
                       }

    def flip_frames(self, frames):
        new_frames_x = []
        new_frames_y = []
        for frame in frames:
            flipped_frames_x = pygame.transform.flip(frame, True, False)
            new_frames_x.append(flipped_frames_x)

        for frame1 in frames:
            flipped_frames_y = pygame.transform.flip(frame1, False, True)
            new_frames_y.append(flipped_frames_y)

        return new_frames_x, new_frames_y

    def create_particles(self, animation_type, pos, group):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, group)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, group, z=LAYERS['main']):
        super().__init__(group)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 1
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = z

    def animate(self, dt):
        self.frame_index += 14 * self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            self.kill()

        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
