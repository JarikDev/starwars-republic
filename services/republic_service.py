import random

from confluent_kafka import Consumer
from confluent_kafka import KafkaException
from confluent_kafka.cimpl import Producer

from model.model import ActionMessage
from services.data_provider import DataProvider


class RepublicService:
    def __init__(self, data_provider: DataProvider, bootstrap_servers, action_topic):
        self.__data_provider = data_provider
        self.__bootstrap_servers = bootstrap_servers
        self.__action_topic = action_topic
        self.__kafka_cfg = {
            'bootstrap.servers': self.__bootstrap_servers,
            'group.id': 'republic',
            'auto.offset.reset': 'earliest'
        }
        self.__consumer = Consumer(self.__kafka_cfg)
        self.__producer = Producer(self.__kafka_cfg)

    def run(self):
        self.__consumer.subscribe([self.__action_topic])
        try:
            while True:
                msg = self.__consumer.poll(timeout=1.0)  # ожидание сообщения
                if msg is None:  # если сообщений нет
                    continue
                if msg.error():  # обработка ошибок
                    raise KafkaException(msg.error())
                else:
                    # действия с полученным сообщением
                    print(f"Received message: {msg.value().decode('utf-8')}")
                    action_msg = ActionMessage.from_json(msg.value().decode('utf-8'))
                    # print(action_msg.action)
                    # jsoned = action_msg.to_json()
                    # print(jsoned)
                    if self.__is_my_turn(action_msg):
                        self.__step()
                        finished_msg = ActionMessage.get_finished_msg()
                        self.__send(self.__action_topic, finished_msg.to_json())
        except KeyboardInterrupt:
            pass
        finally:
            self.__consumer.close()  # не забываем закрыть соединение

    def __is_my_turn(self, action_msg: ActionMessage):
        return action_msg.allegiance == "REPUBLIC" and action_msg.action == "START"

    def __send(self, topic, message_str):
        self.__producer.produce(topic, message_str)
        self.__producer.flush()

    def __step(self):
        systems = self.__data_provider.request_star_systems()
        for system in systems:
            ally_fleet = self.__data_provider.request_fleet(system, "REPUBLIC", "ACTIVE")
            enemy_fleet = self.__data_provider.request_fleet(system, "SEPARATIST", "ACTIVE")
            stalling_ships = []
            if len(enemy_fleet) > 0:
                for ship in ally_fleet:
                    enemy_ship = random.choice(enemy_fleet)
                    attack_msg = ship.get_attack_msg(enemy_ship.id, enemy_ship.ship_class)
                    self.__send(self.__action_topic, attack_msg.to_json())
            else:
                stalling_ships.extend(ally_fleet)

            stalling_units = []
            contested_planets = {}
            planets = self.__data_provider.request_planets(system)
            for planet in planets:
                enemies = self.__data_provider.request_units(planet, "SEPARATIST", "ACTIVE")
                if len(enemies) > 0:
                    contested_planets[planet] = enemies

            for planet in planets:
                allies = self.__data_provider.request_units(planet, "REPUBLIC", "ACTIVE")
                if planet in contested_planets:
                    enemies = contested_planets[planet]
                    for ally in allies:
                        enemy_unit = random.choice(enemies)
                        attack_msg = ally.get_attack_msg(enemy_unit.id, enemy_unit.unit_class)
                        self.__send(self.__action_topic, attack_msg.to_json())
                    for ship in stalling_ships:
                        enemy_unit = random.choice(enemies)
                        attack_msg = ship.get_attack_msg(enemy_unit.id, enemy_unit.unit_class)
                        self.__send(self.__action_topic, attack_msg.to_json())
                else:
                    stalling_units.extend(allies)

            if len(contested_planets.keys()) > 0:
                if len(stalling_ships) > 0:
                    if len(stalling_units) > 0:
                        to_planet_name = next(iter(contested_planets))
                        to_planet = self.__data_provider.request_planet_by_name(to_planet_name)
                        for unit in stalling_units:
                            move_msg = unit.get_move_msg(to_planet.id)
                            # ser_move_msg = json.dumps(move_msg).encode('utf-8')
                            self.__send(self.__action_topic, move_msg.to_json())
            else:
                contested_systems = self.__data_provider.request_contested_star_systems("SEPARATIST")
                if len(contested_systems) > 0:
                    to_system_name = contested_systems[0]
                    to_system = self.__data_provider.request_star_system(to_system_name)
                    if len(stalling_ships) > 0:
                        for ship in stalling_ships:
                            move_msg = ship.get_move_msg(to_system.id)
                            self.__send(self.__action_topic, move_msg.to_json())
                    if len(stalling_units) > 0:
                        planets = self.__data_provider.request_planets(system)
                        planet = self.__data_provider.request_planet_by_name(random.choice(planets))
                        for unit in stalling_units:
                            move_msg = unit.get_move_msg(planet.id)
                            self.__send(self.__action_topic, move_msg.to_json())
                else:
                    victoryMsg = ActionMessage.get_victory_msg()
                    self.__send(self.__action_topic, victoryMsg.to_json())
