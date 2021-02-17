# coding:cp1251
from logic.utils import load_data, create_browser
from mechanize import Browser
from bs4 import BeautifulSoup
from constants import (STATION_LIST_DIR_KZ, STATION_LIST_DIR_RU, ROOT_DIR, USERNAME, PASSWORD)
import re, json, ast
from decimal import Decimal
from yandex_geocoder import Client

class Coordinator:
    def __init__(self):
        self.regions = load_data('../stations/station_ids full.json')
        self.client = Client("6f93606d-8948-4c52-8db6-363d427c0571")

    def get_location(self):
        coordinates = self.client.coordinates("Москва Льва Толстого 16")
        assert coordinates == (Decimal("37.587093"), Decimal("55.733969"))

crdntr = Coordinator()
crdntr.get_location()

# 6f93606d-8948-4c52-8db6-363d427c0571