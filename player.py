import pygame
from settings import *
from support import *
from timer import Timer
from entity import Entity


class Player(Entity):
    def __init__(self, pos, group, collision_sprites, create_magic):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.z = LAYERS['main']

        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-40, -50))

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # tools/weapons
        self.timers = {'tool use': Timer(700, self.use_tool),
                       'tool switch': Timer(200),
                       'magic use': Timer(700),
                       'magic switch': Timer(200)
                       }

        # available tools
        self.tools = ['magic', 'weapon']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]
        self.can_switch_tool = True

        # magic
        # remember this line
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())
        self.selected_magic = self.magic[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats

        self.stats = {'health': 100, 'energy': 100, 'attack': 4, 'magic': 2, 'speed': 250}
        self.health = self.stats['health']  # * 0.8
        self.energy = self.stats['energy']  # * 0.5
        self.exp = 123
        self.speed = self.stats['speed']
        self.animation_speed = 1.5

        # damage tomer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerabity_duration = 500

    def import_assets(self):
        self.animations = {'die': [], 'down': [], 'down_idle': [], 'left_idle': [],
                           'right_idle': [], 'up_idle': [], 'left': [], 'down_magic': [],
                           'left_magic': [], 'right_magic': [], 'up_magic': [], 'right': [],
                           'up': [], 'down_weapon': [], 'up_weapon': [], 'left_weapon': [], 'right_weapon': []}

        for animation in self.animations.keys():
            full_path = 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\characters\\' + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        # vertical movement
        if not self.timers['tool use'].active:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # horizontal movement
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'

            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # tool_use/ weapon use
            if keys[pygame.K_r] and not self.attacking:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                # self.use_tool()

                # change tool

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1

                if self.tool_index < len(self.tools):
                    self.tool_index = self.tool_index
                else:
                    self.tool_index = 0
                # print(self.tool_index)
                self.selected_tool = self.tools[self.tool_index]

            # Magic use

            if keys[pygame.K_f] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.timers['magic use'].activate()
                self.direction = pygame.math.Vector2()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
                self.frame_index = 0

            # change_magic
            if keys[pygame.K_e] and not self.timers['magic switch'].active:
                self.timers['magic switch'].activate()
                self.magic_index += 1

                if self.magic_index < len(self.magic):
                    self.magic_index = self.magic_index
                else:
                    self.magic_index = 0
                self.selected_magic = self.magic[self.magic_index]
                # print(self.selected_magic)

    # remember this function/method
    def use_tool(self):
        pass

    def animate(self, dt):
        self.frame_index += 9 * dt * self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

        # FILCKERING ON HIT
        if not self.vulnerable:
            alpha = self.flickering()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # needs refactoring
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # TOOL USE
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + 'weapon'

        # MAGIC USE
        if self.timers['magic use'].active:
            self.status = self.status.split('_')[0] + '_' + 'magic'

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.selected_magic]['strength']

        return base_damage + spell_damage

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update_timers(self):
        current_time = pygame.time.get_ticks()
        for timer in self.timers.values():
            timer.update()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerabity_duration:
                self.vulnerable = True

    # def collision(self, direction):
    #     for sprite in self.collision_sprites.sprites():
    #         if hasattr(sprite, 'hitbox'):
    #             if sprite.hitbox.colliderect(self.hitbox):
    #
    #                 # horizontal collision
    #                 if direction == 'horizontal':
    #                     if self.direction.x > 0:  # moving right
    #                         self.hitbox.right = sprite.hitbox.left
    #                     if self.direction.x < 0:  # moving left
    #                         self.hitbox.left = sprite.hitbox.right
    #
    #                     self.rect.centerx = self.hitbox.centerx
    #                     self.pos.x = self.hitbox.centerx
    #
    #                 # vertical collision
    #                 if direction == 'vertical':
    #                     if self.direction.y > 0:  # down
    #                         self.hitbox.bottom = sprite.hitbox.top
    #                     if self.direction.y < 0:  # moving up
    #                         self.hitbox.top = sprite.hitbox.bottom
    #
    #                     self.rect.centery = self.hitbox.centery
    #                     self.pos.y = self.hitbox.centery
    #
    # def move(self, dt):
    #     if self.direction.magnitude() > 0:
    #         self.direction = self.direction.normalize()
    #
    #     # horizontal movement
    #     self.pos.x += self.direction.x * self.speed * dt
    #     self.hitbox.centerx = round(self.pos.x)
    #     self.rect.centerx = self.hitbox.centerx
    #     self.collision('horizontal')
    #
    #     # vertical movement
    #     self.pos.y += self.direction.y * self.speed * dt
    #     self.hitbox.centery = round(self.pos.y)
    #     self.rect.centery = self.hitbox.centery
    #     self.collision('vertical')

    def update(self, dt):
        self.input()
        self.cooldowns()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
        self.energy_recovery()
