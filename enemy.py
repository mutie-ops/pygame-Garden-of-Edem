from settings import *
from entity import Entity
import pygame
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, group, z, collision_sprites, damage_player, trigger_enemy_death):
        super().__init__(group)
        # GRAPHICS SETUP
        self.import_graphics(monster_name)
        self.z = LAYERS['main']
        self.status = 'down_idle'
        self.frame_index = 0
        self.sprite_type = 'enemy'
        self.animation_speed = 3
        self.image = self.animations[self.status][self.frame_index]
        self.trigger_enemy_death = trigger_enemy_death

        # MOVEMENT
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)

        # ENEMY HITBOX
        self.hitbox = self.rect.copy().inflate((-40, -50))
        self.collision_sprites = collision_sprites

        self.attack_sprites = pygame.sprite.Group()
        self.attack_able_sprites = pygame.sprite.Group()

        # STATS
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.damage = monster_info['damage']
        self.attack_type = monster_info['attack_type']
        self.speed = monster_info['speed']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        # ATTACK/ player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # INVINCIBILITY TIMER
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'die': [], 'down_attack': [], 'down_idle': [], 'left_idle': [],
                           'right_idle': [], 'up_idle': [], 'left_attack': [], 'right_attack': [],
                           'up_attack': [], 'down_walk': [], 'up_walk': [], 'left_walk': [], 'right_walk': []}

        for animation in self.animations.keys():
            full_path = 'C:\\Users\\benja\\Desktop\\pythonProject\\tiles\\enemy\\' + animation
            self.animations[animation] = import_folder(full_path)

    # get player distance and direction from enemy
    def get_player_distance_direction(self, player):

        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction, player_vector

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]

        if direction.x <= -0.7:

            self.status = 'left'

        elif direction.x >= 0.7:
            self.status = 'right'

        if direction.y >= 0.7:
            self.status = 'down'

        elif direction.y <= -0.7:
            self.status = 'up'

        if distance < self.attack_radius:
            self.status = self.status.split('_')[0] + '_attack'

        elif distance < self.notice_radius:
            self.status = self.status.split('_')[0] + '_walk'

            # self.status = 'walk'
        else:
            self.status = self.status.split('_')[0] + '_idle'

    def actions(self, player):
        # if self.status == 'attack':'
        if self.status == self.status.split('_')[0] + '_attack':
            self.attack_time = pygame.time.get_ticks()
            # print('attack')
            self.damage_player(amount=self.damage, attack_type=self.attack_type)

        elif self.status == self.status.split('_')[0] + '_walk':
            # move towards player
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self, dt):
        animation = self.animations[self.status]

        self.frame_index += 9 * dt * self.animation_speed
        if self.frame_index > len(animation):
            if self.status == self.status.split('_')[0] + '_attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # FLICKERING ON HIT
        if not self.vulnerable:
            alpha = self.flickering()  # flicker
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'magic':
                self.health -= player.get_full_magic_damage()
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            pos = self.rect.center
            self.trigger_enemy_death(pos, self.monster_name)
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def enemy_update(self, player):

        self.get_status(player)
        self.actions(player)
        self.cooldown()
        self.check_death()

    def update(self, dt):
        self.hit_reaction()
        self.move(self.speed)
        self.animate(dt)
