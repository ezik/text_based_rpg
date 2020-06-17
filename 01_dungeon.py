# -*- coding: utf-8 -*-

from entities import Player
from decimal import Decimal
import time
from utils import load_json_data, get_location_dependencies, get_monsters_positions, remove_monster, print_entities, \
    location_empty, write_players_data

remaining_time = '123456.0987654321'
field_names = ['current_location', 'current_experience', 'current_date']

json_data = load_json_data('./rpg.json')
locations_dict = get_location_dependencies(json_data)
monsters_dict = get_monsters_positions(json_data)

player = Player(remaining_time=remaining_time)
game = True

while game:
    print('*' * 30)

    if Decimal(player.remaining_time) < 0:
        print('У тебя не осталось времени герой. Сложи свой меч и возродись как птица Феникс.')
        print('*' * 30)
        player.reset(remaining_time=remaining_time)

    print(f'Ты находишься в {player.location}.\n'
          f'У тебя {player.experience} очков опыта, осталось {player.remaining_time} секунд до наводнения.\n'
          f'Прошло времени: {player.show_time_passed()}\n')
    player.store_player_data()

    if location_empty(locations_dict, monsters_dict, player.location):
        print('Герой, ты остался наедине с пустотой. Время уходит и тебе уже не выбраться. '
              'Сложи свой меч и возродись как Феникс.')
        print('*' * 30)
        player.reset(remaining_time=remaining_time)

    print_entities(locations_dict, monsters_dict, player.location)
    print('\nВыбери действие:')
    player.help(locations_dict, monsters_dict)
    line = input('>> ')
    args = line.split()
    if args[0] == '1':
        player.attack(monsters_dict[player.location])
        remove_monster(monsters_dict, player.location, player.last_attacked_monster)
    elif args[0] == '2':
        player.change_location(locations_dict[player.location])
    elif args[0] == '3':
        write_players_data(field_names=field_names, player_data=player.player_data)
        player.exit()

    if player.location == 'Hatch_tm159.098765432' and player.experience >= 280:
        print('Вот это да! Ты вышел из подземелий даже не замочив ботинок! '
              'Спеши же к принцессе, она накормит тебя восхитительным обедом."')
        time.sleep(1)
        game = False
        write_players_data(field_names=field_names, player_data=player.player_data)
        player.exit()

    elif player.location == 'Hatch_tm159.098765432' and player.experience < 280:
        print('*'*30)
        print('Герой, все двери за тобой захлопнулись.\nВода уже близко и люк не откроется просто так.\n'
              'Сложи свой меч и возродись как Феникс.\n')
        player.reset(remaining_time=remaining_time)
