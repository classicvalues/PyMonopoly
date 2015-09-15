# -*- coding: utf-8 -*-
import Globals
from pygame import Color, display, mixer
from os import listdir
from sys import exit as SYSEXIT

#--- Common
def change_color_alpha(color, alpha):
    color -= Globals.COLORS['black']
    color.a = alpha
    return color
def change_volume(volume, write_to_file=False):
    mixer.music.set_volume(volume)
    Globals.SOUNDS['button-pressed'].set_volume(volume)
    Globals.SETTINGS['volume'] = volume
    if write_to_file:
        save_settings()
def switch_sound_state(object, current, write_to_file=False):
    if object == 'music':
        if current:
            mixer.music.fadeout(2000)
        else:
            mixer.music.play(-1)
    Globals.SETTINGS[object] = not current
    if write_to_file:
        save_settings()
def play_click_sound():
    if Globals.SETTINGS['sounds']:
        Globals.SOUNDS['button-pressed'].play()
def slight_animation_count_pos(new, current, speed):
    if new != current:
        current = list(current)
        for axis in range(2):
            if new[axis] != current[axis]:
                diff = (new[axis] - current[axis])/speed
                if abs(diff) < 0.1:
                    diff = 1
                current[axis] += diff
    return tuple(current)
def read_file(file):
    list = open(file, 'r')
    array = list.readlines()
    list.close()
    return map(lambda x: x.decode('UTF').strip('\n'), array)
def write_to_file(file, data, method='w'):
    list = open(file, method)
    list.writelines(map(lambda x: x.encode('UTF'), data))
    list.close()
#--- Hardware related
def check_user_monitor(x, y):
    if display.Info().current_w-70 < x or display.Info().current_h-60 < y:
        print("Your monitor has too small resolution! We can't provide a good interface for it :(")
        SYSEXIT()
    else:
        return (x, y)
#--- Statistics, settings and translations
def check_files():
    DB = listdir(Globals.DIRS['settings'])
    for FILE in ('stats', 'settings', 'last_game_settings'):
        if FILE not in DB:
            create_init_file(FILE)
def create_init_file(type):
    if type == 'stats':
        data = ['0\n' if x<3 else 'None 0 01.01.01 black\n' for x in range(10)]
        data = ['0\n'] + data + ['1\n'] + data
    elif type == 'settings':
        data = ('0\n', 'Player 1\n', '255\n', '30\n', '30\n', '1\n', '1\n', '1\n', '1.0\n', '1\n')
    elif type == 'last_game_settings':
        data = ("3\n", "2\n")
    write_to_file(Globals.FILES[type], data)
def read_settings():
    SETTINGS = read_file(Globals.FILES['settings'])
    return {'language'  : int(SETTINGS[0]),
            'pl_name'   : SETTINGS[1],
            'pl_color'  : Color(int(SETTINGS[2]), int(SETTINGS[3]), int(SETTINGS[4])),
            'fav_game'  : int(SETTINGS[5]),
            'music'     : bool(int(SETTINGS[6])),
            'sounds'    : bool(int(SETTINGS[7])),
            'volume'    : float(SETTINGS[8]),
            'block'     : bool(int(SETTINGS[9]))}
def save_settings():
    array = [str(Globals.SETTINGS['language']) + '\n',
             Globals.SETTINGS['pl_name'] + '\n',
             str(Globals.SETTINGS['pl_color'][0]) + '\n',
             str(Globals.SETTINGS['pl_color'][1]) + '\n',
             str(Globals.SETTINGS['pl_color'][2]) + '\n',
             str(Globals.SETTINGS['fav_game']) + '\n',
             str(int(Globals.SETTINGS['music'])) + '\n',
             str(int(Globals.SETTINGS['sounds'])) + '\n',
             str(Globals.SETTINGS['volume']) + '\n',
             str(int(Globals.SETTINGS['block'])) + '\n']
    write_to_file(Globals.FILES['settings'], array)
def read_translation(lang):
    return read_file(Globals.DIRS['translations'] + Globals.LANGUAGES[lang][0] + '/main')
def read_stats(game):
    array = read_file(Globals.FILES['stats'])
    #--- 0: monopoly, 10: manager
    if game:
        line = 0
    else:
        line = 10
    for i in range(line, line+10):
        if i < line+3:
            array[i] = int(array[i])
        else:
            temp = array[i].split()
            array[i] = {'name'      : temp[0],
                        'score'     : int(temp[1]),
                        'date'      : temp[2],
                        'recent'    : bool(int(temp[3]))}
    return array[line:line+10]
