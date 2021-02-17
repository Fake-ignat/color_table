# coding:cp1251
from logic.utils import load_data
from constants import STATION_LIST_DIR_RU
import json
from yandex_geocoder import Client

class YandexGeocoder:
    def __init__(self):
        self.regions = load_data(STATION_LIST_DIR_RU)
        self.client = Client("c0d403ab-e5be-4049-908c-8122a58acf23")

    def get_location(self, station, region=''):
        try:
            lat, long = map(float, self.client.coordinates(f"{region} {station}"))
            return [lat, long]
        except Exception:
            print(Exception)

    def update_regions(self):
        for region, station_data in self.regions.items():
            for station, station_id in station_data.items():
                locations = self.get_location(station, region)
                if locations:
                    new_data = dict(id=station_id, location=locations)
                    self.regions[region][station] = new_data
                    print(f'{region} - {station}: координаты обновлены!')
                else:
                    self.regions[region][station] = dict(id=station_id, location=None)
                    print(f'{region} - {station}: ненаход')

    def save_data(self):
        filename = '../stations/ru_meteo_yandex_locatons.json'
        with open(filename, 'w') as f:
            json.dump(self.regions, f, indent=2, ensure_ascii=False)


geocoder = YandexGeocoder()
geocoder.update_regions()
geocoder.save_data()

# 6f93606d-8948-4c52-8db6-363d427c0571