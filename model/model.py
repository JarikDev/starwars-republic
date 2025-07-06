import random
from abc import abstractmethod
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


class Actionable:
    @abstractmethod
    def get_attack_msg(self, enemy_id, enemy_class):
        pass

    @abstractmethod
    def get_move_msg(self, planet_id):
        pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ActionMessage:
    allegiance: str
    unit_id: int
    target_id: int
    unit_class: str
    target_class: str
    action: str

    def __init__(self, allegiance, unit_id, target_id, unit_class, target_class, action):
        self.allegiance = allegiance
        self.unit_id = unit_id
        self.target_id = target_id
        self.unit_class = unit_class
        self.target_class = target_class
        self.action = action

    @staticmethod
    def get_victory_msg():
        return ActionMessage("REPUBLIC", None, None, None, None, "WON")

    @staticmethod
    def get_finished_msg():
        return ActionMessage("REPUBLIC", None, None, None, None, "FINISHED")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StarSystem:
    id: int
    name: str
    planet_reports: list
    ship_reports: list

    def __init__(self, id, name, planet_reports, ship_reports):
        self.id = id
        self.name = name
        self.planet_reports = planet_reports
        self.ship_reports = ship_reports

    def get_attack_msg(self, enemy_id, enemy_class):
        pass

    def get_move_msg(self, planet_id):
        pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Planet:
    id: int
    name: str
    allegiance: str
    star_system: str
    unit_reports: list
    hero_reports: list

    def __init__(self, id, name, allegiance, star_system, unit_reports, hero_reports):
        self.id = id
        self.name = name
        self.allegiance = allegiance
        self.star_system = star_system
        self.unit_reports = unit_reports
        self.hero_reports = hero_reports

    def get_attack_msg(self, enemy_id, enemy_class):
        pass

    def get_move_msg(self, planet_id):
        pass

    @staticmethod
    def map_from_json(jsn):
        return Planet(int(jsn['id']), jsn['name'], jsn['allegiance'], jsn['starSystem'], jsn['unitReports'],
                      jsn['heroReports'])


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Ship:
    id: int
    name: str
    allegiance: str
    ship_class: str
    star_system: str
    hp: float
    total_damage: float
    status: str

    def __init__(self, id, name, allegiance, ship_class, star_system, hp, total_damage, status):
        self.id = id
        self.name = name
        self.allegiance = allegiance
        self.ship_class = ship_class
        self.star_system = star_system
        self.hp = hp
        self.total_damage = total_damage
        self.status = status

    def get_attack_msg(self, enemy_id, enemy_class):
        return ActionMessage("REPUBLIC", self.id, enemy_id, self.ship_class, enemy_class, "ATTACK")

    def get_move_msg(self, star_system_id):
        return ActionMessage("REPUBLIC", self.id, star_system_id, self.ship_class, None, "MOVE")

    def attack_enemy_fleet(self, enemy_fleet: list):
        enemy_ship = random.choice(enemy_fleet)
        return self.get_attack_msg(enemy_ship.id, enemy_ship.ship_class)

    @staticmethod
    def map_from_json(jsn):
        return Ship(jsn['id'], jsn['name'], jsn['allegiance'], jsn['shipClass'], jsn['starSystem'], jsn['hp'],
                    jsn['totalDamage'], jsn['status'])


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Unit:
    id: int
    name: str
    allegiance: str
    unit_class: str
    planet: str
    hp: float
    total_damage: float
    status: str

    def __init__(self, id, name, allegiance, unit_class, planet, hp, total_damage, status):
        self.id = id
        self.name = name
        self.allegiance = allegiance
        self.unit_class = unit_class
        self.planet = planet
        self.hp = hp
        self.total_damage = total_damage
        self.status = status

    def get_attack_msg(self, enemy_id, enemy_class):
        return ActionMessage("REPUBLIC", self.id, enemy_id, self.unit_class, enemy_class, "ATTACK")

    def get_move_msg(self, planet_id):
        return ActionMessage("REPUBLIC", self.id, planet_id, self.unit_class, None, "MOVE")

    def attack_enemy_fleet(self, enemy_fleet: list):
        enemy_ship = random.choice(enemy_fleet)
        return self.get_attack_msg(enemy_ship.id, enemy_ship.ship_class)

    @staticmethod
    def map_from_json(jsn):
        return Unit(jsn['id'], jsn['name'], jsn['allegiance'], jsn['unitClass'], jsn['planet'], jsn['hp'],
                    jsn['totalDamage'],
                    jsn['status'])
