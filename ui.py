import pygame
from settings import *
from player import Player


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.tool_graphics = []
        for tool in tool_data.values():
            path = tool['graphics']
            tool = pygame.image.load(path).convert_alpha()
            self.tool_graphics.append(tool)

        self.magic_graphics = []
        for magic in magic_data.values():
            path2 = magic['graphics']
            magic = pygame.image.load(path2).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # converting stats to pixels
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar rect
        pygame.draw.rect(self.display_surface, color, current_rect)

        # draw bar rect border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surface = self.font.render('Edems : ' + str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 30
        y = self.display_surface.get_size()[1] - 25
        text_rect = text_surface.get_rect(bottomright=(x, y))
        # pygame.draw.rect(self.display_surface, UI_BG_COLOR,text_rect.inflate(20,0))
        self.display_surface.blit(text_surface, text_rect)
        # pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(20,0),3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    # weapon/tool overlay
    def weapon_overlay(self, tool_index, switched):
        bg_rect = self.selection_box(10, 630, switched)  # WEAPON/TOOL
        tool_surf = self.tool_graphics[tool_index]
        tool_rect = tool_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(tool_surf, tool_rect)

        # MAGIC OVERLAY

    def magic_overlay(self, magic_index, switched):
        bg_rect = self.selection_box(100, 630, switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.weapon_overlay(player.tool_index, not player.can_switch_tool)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        # self.selection_box(100, 630)  # MAGIC
