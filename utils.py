import json
import re
import csv
from collections import defaultdict
from sys import exit


def load_json_data(file):
    """
    :param file: json file
    :return: parsed json data
    """
    try:
        with open(file, 'r') as read_json:
            return json.load(read_json)
    except FileNotFoundError:
        print("Такого файла нет. Проверь путь и название.")
        exit()


def generate_locations_list(json_data):
    """
    :param json_data: parsed json data
    :return: locations list generated from data
    """
    pattern = r'Location_\w*_tm[^a-zA-Z]*\d|Hatch_tm\d+.\d+'
    keys_lookup = str(json_data)
    return re.findall(pattern, keys_lookup)


def parse_locations_data(json_data, lookup_key):
    """
    :param json_data: parsed json
    :param lookup_key: root player's location given in Player.__init__
    :return: value for given key
    """
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == lookup_key:
                yield v
            else:
                yield from parse_locations_data(v, lookup_key)
    elif isinstance(json_data, list):
        for item in json_data:
            yield from parse_locations_data(item, lookup_key)


def get_location_dependencies(json_data):
    """
    :param json_data: parsed json
    :return: locations dict as {location: [location1, location2, etc]}
    """
    locations_dict = defaultdict(list)
    locations_list = generate_locations_list(json_data)

    for location in locations_list:
        for data in parse_locations_data(json_data, location):
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        locations_dict[location].extend([str(k) for k in item.keys()])
    return locations_dict


def get_monsters_positions(json_data):
    """
    :param json_data: parsed json
    :return: monsters dict as {location: [monster1, monster2, etc]}
    """
    monsters_dict = defaultdict(list)
    locations_list = generate_locations_list(json_data)  # вывести единый список ключей для обоих диктов
    for location in locations_list:
        for data in parse_locations_data(json_data, location):
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        monsters_dict[location].append(item)
    return monsters_dict


def remove_monster(d, key, value):
    """
    :param d: monsters dict
    :param key: player location
    :param value: last attacked monster
    :return: None
    """
    try:
        d[key].remove(value)
    except ValueError:
        pass


def location_empty(d1, d2, key):
    """
    :param d1: locations dict
    :param d2: monsters dict
    :param key: player location
    :return:
    """
    if len(d1[key]) == 0 and len(d2[key]) == 0:
        return True


def print_entities(d1, d2, key):
    """
    :param d1: locations dict
    :param d2: monsters dict
    :param key: player current location
    :return: None
    """
    d1set = set(d1)
    d2set = set(d2)
    print('Внутри ты видишь:')
    if key in d1set.intersection(d2set):
        for value in d1[key]:
            print(f'— Вход в локацию: {value}')
        for value in d2[key]:
            print(f'— Монстра: {value}')
    elif key in d1set:
        for value in d1[key]:
            print(f'— Вход в локацию: {value}')
    elif key in d2set:
        for value in d2[key]:
            print(f'— Монстра: {value}')


def write_players_data(field_names, player_data):
    """
    :param field_names: file header passed as list
    :param player_data: player data, list
    :return: None
    """
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_names)
        writer.writerows(player_data)
