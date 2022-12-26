import pygame
from settings import *
from player import Player
from sprites import Generic, Tree, Rock, House, Light
from pytmx.util_pygame import load_pygame
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer


class Level:
    def __init__(self):

        # ATTACKING
        self.attack_sprites = pygame.sprite.Group()
        self.attack_able_sprites = pygame.sprite.Group()

        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.map_area_1()
        self.ui = UI()

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def map_area_1(self):
        tmx_data = load_pygame('/tiles/tmx/map2.tmx')
        # collisions
        for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
            Generic((x * 16, y * 16), pygame.Surface((16,16)), self.collision_sprites)

        # PLAYER
        for player in tmx_data.get_layer_by_name('start'):
            self.player = Player((player.x, player.y), self.all_sprites, self.collision_sprites, self.create_magic)

        # ENEMY
        for enemy in tmx_data.get_layer_by_name('marker'):
            self.enemy = Enemy(monster_name='goblin_general',
                               pos=(enemy.x, enemy.y),
                               group=[self.all_sprites, self.attack_able_sprites],
                               z=LAYERS['main'],
                               collision_sprites=self.collision_sprites, damage_player=self.damage_player,
                               trigger_enemy_death=self.trigger_enemy_death)

        # PLANTS
        for x, y, surf in tmx_data.get_layer_by_name('ground_plants').tiles():
            Generic(pos=(x * 16, y * 16), surf=surf, group=self.all_sprites, z=LAYERS['ground_plants'])

        # TREES
        for obj in tmx_data.get_layer_by_name('trees'):
            self.tree = Tree(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites, self.collision_sprites],
                             name=obj.name)

        #  HILLS
        for x, y, surf in tmx_data.get_layer_by_name('hills').tiles():
            Generic(pos=(x * 16, y * 16), surf=surf, group=self.all_sprites, z=LAYERS['hills'])

        # ROCKS AND TREE CUT
        for obj in tmx_data.get_layer_by_name('rocks and tree cut'):
            self.rock = Rock(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites, self.collision_sprites],
                             name=obj.name)

        # HOUSES
        for obj in tmx_data.get_layer_by_name('houses'):
            if obj.image:
                self.house = House(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites])

        # LIGHTS
        for obj in tmx_data.get_layer_by_name('lights'):
            self.light = Light(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites])
        # for x, y, surf in tmx_data.get_layer_by_name('ground').tiles():
        #     Generic((x * 16, y * 16), surf=surf, group=self.all_sprites)

        Generic(pos=(0, 0),
                surf=pygame.image.load(
                    '/tiles/world/map3.png').convert_alpha(),
                group=self.all_sprites,
                z=LAYERS['ground'])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.all_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.all_sprites, self.attack_sprites])

        if style == 'die':
            print(style)
            print(strength)
            print(cost)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:

                # needs redo from pydew valley tutorial
                collision_sprites = pygame.sprite.spritecollide(sprite=attack_sprite
                                                                , group=self.attack_able_sprites
                                                                , dokill=False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles
            pos = self.player.rect.center
            self.animation_player.create_particles(attack_type, pos, [self.all_sprites])

    def trigger_enemy_death(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player, self.rock, self.enemy, self.tree, self.house)
        self.ui.display(self.player)
        self.all_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.all_sprites.update(dt)


# camera
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, rock, enemy, trees, house):
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        #
        for layer in LAYERS.values():
            for sprite_image in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite_image.z == layer:
                    offset_rect = sprite_image.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite_image.image, offset_rect)
                    # pygame.draw.rect(self.display_surface, 'blue', offset_rect, 5)
                    # self.hitbox = offset_rect.inflate((-95, -100))
                    # pygame.draw.rect(self.display_surface, 'red', self.hitbox, 5)
                    #
                    # # HITBOX VISUALIZATION
                    #
                    # if sprite_image == player:
                    #     self.hitbox = offset_rect.inflate((-40, -50))
                    #     pygame.draw.rect(self.display_surface, 'green', self.hitbox, 5)
                    # #
                    # # if sprite_image == tree:
                    # #     self.hitbox = offset_rect.inflate((-100, -100))
                    # #     # pygame.draw.rect(self.display_surface, 'red', self.hitbox, 5)
                    #
                    # if sprite_image == rock:
                    #     self.hitbox = offset_rect.inflate(-25, -40)
                    #     # pygame.draw.rect(self.display_surface, 'blue', self.hitbox, 5)
                    # if sprite_image == enemy:
                    #     self.hitbox = offset_rect.inflate(-40, -50)
                    #     pygame.draw.rect(self.display_surface, 'green', self.hitbox, 5)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
