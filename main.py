import pygame.display
from players import *
import sys
import pytmx
from pytmx.util_pygame import load_pygame
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Garden of Edem')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    # map = load_pygame('C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\tmx\\trialmap.tmx')
    #
    #
    # # load data
    # def load_map1(tiled_map):
    #     for layer in tiled_map.layers:
    #         if isinstance(layer, pytmx.TiledTileLayer):
    #             for x, y, tile in layer.tiles():
    #                 if tile:
    #                     display_surface.blit(tile, (x * 16 + 120, y * 16))
    #
    #
    # def load_tree_objects(tiled_map):
    #     for obj in tiled_map.objects:
    #         if obj.name == 'tree':
    #             # # for sprite in sorted(obj,key = lambda sprite: obj.y)
    #             rect = pygame.Rect(obj.x + 120, obj.y, obj.width, obj.height)
    #             hitbox = rect.copy().inflate(-220, rect.height - 480)
    #             display_surface.blit(obj.image, rect)
    #             # pygame.draw.rect(display_surface, '#17ddee', hitbox)
    #
    #
    # def load_rock_objects(tiled_map):
    #     for obj in tiled_map.objects:
    #         if obj.name == 'rocks':
    #             # # for sprite in sorted(obj,key = lambda sprite: obj.y)
    #             rect = pygame.Rect(obj.x + 120, obj.y, obj.width, obj.height)
    #             hitbox = rect.copy().inflate(-220, rect.height - 480)
    #             display_surface.blit(obj.image, rect)
    #             # pygame.draw.rect(display_surface, '#17ddee', hitbox)
    #
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
