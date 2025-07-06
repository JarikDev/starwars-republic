import requests

from model.model import Planet, Unit, StarSystem, Ship


class DataProvider:

    def __init__(self):
        self.__star_wars_host = "http://localhost:7100"
        self.__star_systems_url = "/star-systems"
        self.__star_system_url = "/star-systems/%s"  # /star-systems/{starSystemName}
        self.__planets_by_star_system_url = "/star-systems/%s/planets"
        self.__units_by_planet_url = "/star-systems/%s/planets"
        self.__planet_by_name_url = "/planets/%s"
        self.__units_by_planet_allegiance_status_url = "/planets/%s/%s/%s"  # /planets/{planetName}/{allegiance}/{status}
        self.__fleet_by_star_system_allegiance_status_url = "/star-systems/%s/%s/%s"  # /star-system/{starSystemName}/{allegiance}/{status}
        self.__star_systems_by_allegiance_url = "/star-systems/contested/%s"  # /star-system/{allegiance}

    def get_json_or_empty_resp(self, url):
        try:
            with requests.Session() as s:
                resp = s.get(url=url)
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            print(f"GOT ERROR {e}")
        return []

    def get_data_url(self, path):
        return f'{self.__star_wars_host}{path}'

    def request_star_systems(self):
        url = self.get_data_url(self.__star_systems_url)
        return self.get_json_or_empty_resp(url)

    def request_star_system(self, system_name):
        url = self.get_data_url(self.__star_system_url % system_name)
        try:
            with requests.Session() as s:
                resp = s.get(url=url)
                if resp.status_code == 200:
                    return StarSystem.from_json(resp.text)
        except Exception as e:
            print(f"GOT ERROR {e}")
        return None

    def request_contested_star_systems(self, allegiance):
        url = self.get_data_url(self.__star_systems_by_allegiance_url % allegiance)
        return self.get_json_or_empty_resp(url)

    def request_planets(self, star_system):
        url = self.get_data_url(self.__planets_by_star_system_url % star_system)
        return self.get_json_or_empty_resp(url)

    def request_planet_by_name(self, planet_name):
        url = self.get_data_url(self.__planet_by_name_url % planet_name)
        try:
            with requests.Session() as s:
                resp = s.get(url=url)
                if resp.status_code == 200:
                    return Planet.from_json(resp.text)
        except Exception as e:
            print(f"GOT ERROR {e}")
        return None

    def request_units(self, planet, allegiance, status):
        url = self.get_data_url(self.__units_by_planet_allegiance_status_url % (planet, allegiance, status))
        try:
            with requests.Session() as s:
                resp = s.get(url=url)
                if resp.status_code == 200:
                    return [Unit.map_from_json(jsn) for jsn in resp.json()]
        except Exception as e:
            print(f"GOT ERROR {e}")
        return []

    def request_fleet(self, star_system, allegiance, status):
        url = self.get_data_url(self.__fleet_by_star_system_allegiance_status_url % (star_system, allegiance, status))
        try:
            with requests.Session() as s:
                resp = s.get(url=url)
                if resp.status_code == 200:
                    return [Ship.map_from_json(jsn) for jsn in resp.json()]
        except Exception as e:
            print(f"GOT ERROR {e}")
        return []
