# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import slight_animation_count_pos
from pygame import Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=None):
        self.init_for_group(group, number)
        self.anticolor = Globals.COLORS['white'] - self.color
        self.update_text(text)
        self.init_new_pos(group)
    def init_for_group(self, group, number):
        self.AV = True
        #--- Fonts
        if group in ('main_settings_volume_SELECTOR', 'main_settings_player_color_SELECTOR'):
            self.font = Globals.FONTS['ume_16']
        elif group[:4] == 'main' or group in ('stats_game_name', 'main_settings_left_MI', 'main_settings_player'):
            self.font = Globals.FONTS['ubuntu_24']
        elif group == 'stats_common':
            self.font = Globals.FONTS['ubuntu_20']
        elif group in ('APPVERSION', 'authors', 'stats_switch', 'stats_bests', 'settings_left') or 'stats_table' in group:
            self.font = Globals.FONTS['ubuntu_16']
        elif group == 'stats_latest':
            self.font = Globals.FONTS['ume_12']
        else:
            self.font = Globals.FONTS['ubuntu_32']
        #--- Colors
        if group in ('authors', 'stats_switch'):
            self.color = Globals.COLORS['grey']
        elif group == 'main_settings_volume_SELECTOR':
            self.choose_vol_color(number)
        elif group == 'main_settings_player_color_SELECTOR':
            self.color = Globals.PLAYERS_COLORS[number]
        elif group == 'main_settings_player':
            self.color = Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['color']
        else:
            self.color = Globals.COLORS['white']
        #--- Position
        if group == 'main_main':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/4
            self.rect = Rect((0, Globals.RESOLUTION[1]/2+50+35*number), (0, 0))
        elif group == 'stats_common':
            self.x = Globals.RESOLUTION[0]/7
            self.rect = Rect((0, 320 + 25 * number), (0, 0))
        elif 'exit' in group or group == 'main_stats':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/6
            self.rect = Rect((0, Globals.RESOLUTION[1]+50), (0, 0))
        elif group == 'stats_game_name':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3-50
            self.rect = Rect((0, 280), (0, 0))
        elif group == 'stats_switch':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3+85
            self.rect = Rect((0, 280), (0, 0))
        elif 'stats_table' in group:
            self.x = Globals.RESOLUTION[0]/7 + 150*int(group[len(group)-1])
            self.rect = Rect((0, 365 + 20*number), (0, 0))
        elif group == 'main_settings_volume_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 623), (0, 0))
        elif group == 'main_settings_player_color_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 458), (0, 0))
        elif group == 'settings_left':
            self.x = Globals.RESOLUTION[0]/5 - 80
            self.rect = Rect((0, 320 + 55*number), (0, 0))
        elif group == 'main_settings_left_MI':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.rect = Rect((0, 342 + 55*number), (0, 0))
        elif group == 'main_settings_player':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.rect = Rect((0, 397 + 35*number), (0, 0))
        elif group == 'stats_latest':
            self.x = Globals.RESOLUTION[0]/7 + 365
            self.rect = Rect((0, 365 + 20*number), (0, 0))
        elif group == 'stats_bests':
            self.x = Globals.RESOLUTION[0]/7 - 20
            self.rect = Rect((0, 400), (0, 0))
        elif group == 'authors':
            self.x = 'right'
            self.x_offset = 10
            self.rect = Rect((0, Globals.RESOLUTION[1]-26-20*number), (0, 0))
        elif group == 'APPNAME':
            self.x = Globals.PICS['logo'].pos[0] + 110
            self.rect = Rect((0, Globals.PICS['logo'].pos[1] + 10), (0, 0))
        elif group == 'APPVERSION':
            self.x = Globals.PICS['logo'].pos[0] + 112
            self.rect = Rect((0, Globals.PICS['logo'].pos[1] + 50), (0, 0))
    def init_new_pos(self, group):
        if group[:5] in ('main_', 'stats', 'setti'):
            self.new_pos = (self.rect.x, self.rect.y - 100)
        else:
            self.new_pos = self.rect.topleft
    def choose_vol_color(self, num):
        if num > Globals.SETTINGS['volume']*10-1:
            self.color = Globals.COLORS['grey63']
        else:
            self.color = Globals.COLORS['white']
    def RErender(self):
        self.text = self.font.render(self.symbols, True, self.color)
    def move_text(self):
        if self.new_pos != self.rect.topleft:
            self.rect.topleft = slight_animation_count_pos(self.new_pos, self.rect.topleft, 10)
    def update_text(self, text, reset_alpha=True):
        self.symbols = text
        size = self.font.size(text)
        xpos = self.find_xpos(size)
        self.rect = Rect((xpos, self.rect.y), size)
        self.RErender()
        if reset_alpha:
            self.alpha = 5
    def find_xpos(self, size):
        if self.x == 'center':
            return Globals.RESOLUTION[0]/2 + self.x_offset - size[0]/2
        elif self.x == 'right':
            return Globals.RESOLUTION[0] - size[0] - self.x_offset
        else:
            return self.x
    def set_alpha(self):
        if self.alpha != 255:
            self.alpha += 10
        if self.alpha != 255:
            surf = Surface(self.rect.size)
            surf.fill(self.anticolor)
            surf.set_colorkey(self.anticolor)
            surf.blit(self.text, (0, 0))
            surf.set_alpha(self.alpha)
            return surf
        else:
            return self.text
    def render(self, MENU=False):
        if not MENU:
            self.move_text()
        Globals.screen.blit(self.set_alpha(), self.rect.topleft)
