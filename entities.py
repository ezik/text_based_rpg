import re
from sys import exit
from decimal import Decimal
from collections import defaultdict
from datetime import datetime


class Location:
    def __init__(self, full_name):
        self.full_name = full_name
        self.time_to_pass = self.get_time()

    def get_time(self):
        """
        :return: time value parsed from location name
        """
        if self.full_name == 'Hatch_tm159.098765432':
            time_pattern_regex = r'Hatch_tm(\d+.\d+)'
            m = re.match(time_pattern_regex, self.full_name)
            return m.group(1)

        time_pattern_regex = r'Location_(\d+|B+\d)_tm(\d+)'
        m = re.match(time_pattern_regex, self.full_name)
        return m.group(2)


class Player:

    player_data = []

    def __init__(self, remaining_time):
        self.experience = 0
        self.location = 'Location_0_tm0'
        self.remaining_time = remaining_time
        self.last_attacked_monster = ''
        self.time_passed = '0'

    def help(self, d1, d2):
        """
        :param d1: locations dict
        :param d2: monsters dict
        :return: None
        """
        if len(d1[self.location]) == 0:
            print(f'1: {Commands["1"]}\n3: {Commands["3"]}')
        elif len(d2[self.location]) == 0:
            print(f'2: {Commands["2"]}\n3: {Commands["3"]}')
        else:
            for k, v in Commands.items():
                print(f'{k}: {v}')

    def attack(self, args):
        """
        :param args: list of monsters in players current location
        :return: None
        """
        print('Монстры в этой локации:')
        for i, arg in enumerate(args):
            print(f'{i + 1}: {arg}')
        selected_monster = int(input('Введи номер: ')) - 1
        try:
            if args[selected_monster]:
                self.last_attacked_monster = args[selected_monster]
                enemy = Monster(self.last_attacked_monster)
                print(f'Это успешный успех! Теперь {self.last_attacked_monster} скорее мертв чем жив.')
                self.set_experience(enemy.hp)
                self.set_remaining_time(enemy.time_to_pass)
                self.set_time_passed(enemy.time_to_pass)
        except IndexError:
            print('Монстра с таким номером нет в списке. Выбери доступный вариант.')

    def change_location(self, args):
        """
        :param args: list of locations open from current players location
        :return:
        """
        print('Доступные к переходу локации:')
        for i, arg in enumerate(args):
            print(f'{i + 1}: {arg}')
        selected_location = int(input('Введи номер: ')) - 1
        try:
            if args[selected_location]:
                self.location = args[selected_location]
                location = Location(self.location)
                self.set_remaining_time(location.get_time())
                self.set_time_passed(location.get_time())
        except IndexError:
            print('Локации с таким номером нет в списке. Выбери доступный вариант.')

    @staticmethod
    def exit():
        print('Прощай, герой!')
        exit()

    def store_player_data(self):
        self.player_data.append([self.location, self.experience, datetime.now()])

    def set_experience(self, monster_hp):
        """
        :param monster_hp: monsters hp
        :return: player's increased experience
        """
        self.experience += int(monster_hp)
        return self.experience

    def set_remaining_time(self, time):
        """
        :param time: time value taken from Location or Monster name
        :return: remaining time left until player will die
        """
        self.remaining_time = Decimal(self.remaining_time) - Decimal(time)
        return str(self.remaining_time)

    def set_time_passed(self, time):
        """
        :param time: time value taken from Location or Monster name
        :return: None
        """
        self.time_passed = Decimal(self.time_passed) + Decimal(time)

    def show_time_passed(self):
        minutes, sec = divmod(Decimal(self.time_passed), 60)
        return "%02d:%02d" % (minutes, sec)

    def reset(self, remaining_time):
        """
        Sets players data to initial values
        :param remaining_time:
        :return: None
        """
        self.__init__(remaining_time)


Commands = {
    '1': 'Атаковать монстра',
    '2': 'Перейти в другую локацию',
    '3': 'Сдаться и выйти из игры'
}


class Monster:
    def __init__(self, full_name):
        self.full_name = full_name
        self.time_to_pass = self.get_time()
        self.hp = self.get_experience()

    def get_time(self):
        """
        :return: time value parsed from Monster's name
        """
        time_pattern_regex = r'Mob_exp\d+_tm(\d+)|Boss\d*_exp\d+_tm(\d+)'
        m = re.match(time_pattern_regex, self.full_name)
        if m.group(1):
            return m.group(1)
        else:
            return m.group(2)

    def get_experience(self):
        """
        :return: hp value parsed from Monster's name
        """
        exp_pattern_regex = r'Mob_exp(\d+)|Boss\d*_exp(\d+)'
        m = re.match(exp_pattern_regex, self.full_name)
        if m.group(1):
            return m.group(1)
        else:
            return m.group(2)
