import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z=LAYERS['main']):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(0,0)


class Tree(Generic):
    def __init__(self, pos, surf, group, name):
        super().__init__(pos, surf, group)
        self.hitbox = self.rect.copy().inflate(-100, -100)

class Rock(Generic):
    def __init__(self, pos, surf, group, name):
        super().__init__(pos, surf, group)
        self.hitbox = self.rect.copy().inflate(-20, -40)


class House(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)


class Light(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)
