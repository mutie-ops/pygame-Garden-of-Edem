import pygame
from settings import *
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.direction = pygame.math.Vector2()
        self.frame_index = 0
        # self.pos = pygame.math.Vector2(self.rect.center)
        # self.rect = self.image.get_rect(center=self.pos)
        # self.hitbox = self.rect.copy().inflate((-40, -50))
        # #self.pos = pygame.math.Vector2(self.rect.center)
        # #self.collision_sprites = collision_sprites

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):

                    # horizontal collision
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    # vertical collision
                    if direction == 'vertical':
                        if self.direction.y > 0:  # down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def flickering(self):

        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
