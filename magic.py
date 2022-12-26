import pygame
from random import randint
from settings import *


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, group):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles(animation_type='heal', pos=player.rect.center, group=group)

    def flame(self, player, cost, group):
        if player.energy >= cost:
            player.energy -= cost

            # horizontal position

            if player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)

            # vertical position

            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)

            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x == 1:
                    offset_x = (direction.x * i) * 64
                    x = player.rect.centerx + offset_x + randint(- 64 // 3, 64 // 3)
                    y = player.rect.centery + randint(- 64 // 3, 64 // 3)
                    self.animation_player.create_particles('flame', (x, y), group)
                elif direction.x == -1:
                    offset_x = (direction.x * i) * 64
                    x = player.rect.centerx + offset_x + randint(- 64 // 3, 64 // 3)
                    y = player.rect.centery + randint(- 64 // 3, 64 // 3)
                    self.animation_player.create_particles('flame', (x, y), group)

                elif direction.y == 1:
                    offset_y = (direction.y * i) * 64
                    x = player.rect.centerx + randint(- 64 // 3, 64 // 3)
                    y = player.rect.centery + offset_y + randint(- 64 // 3, 64 // 3)
                    self.animation_player.create_particles('flame', (x, y), group)

                else:
                    offset_y = (direction.y * i) * 64
                    x = player.rect.centerx + randint(- 64 // 3, 64 // 3)
                    y = player.rect.centery + offset_y + randint(- 64 // 3, 64 // 3)
                    self.animation_player.create_particles('flame', (x, y), group)

    def wither(self):
        pass
