# coding:cp1251

from mechanize import Browser
from bs4 import BeautifulSoup
from constants import (STATION_LIST_DIR_KZ, STATION_LIST_DIR_RU)
import os, json

class Finder():
    def __init__(self, country='RU'):
        self.br = Finder.create_browser()
        self.country = country
        if self.country == 'RU':
            self.region_list = self.load_regions()
            self.station_ids = self.get_station_list()
        if self.country == 'KZ':
            self.station_ids = self.get_foreign_st_list()

    def load_regions(self):
        region_list = {}
        pref = 'ru' if self.country == 'RU' else 'kz'
        url = f"http://www.pogodaiklimat.ru/archive.php?id={pref}"
        # открываем ссылку с регионами
        try:
            html = self.br.open(url)
            soup = BeautifulSoup(html, "lxml")
            links = soup.findAll("li", {"class": "big-blue-billet__list_link"})
            for link in links:
                href = link.find('a').get('href')
                region_name = link.find('a').text
                if 'region' in href:
                    region_list[region_name] = f'http://www.pogodaiklimat.ru{href}'
        except Exception as e:
            print("[!]Critical, could not open page.")

        return region_list

    @staticmethod
    def create_browser():
        # Создаем браузер и настраиваем
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('user-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                        ' Chrome/79.0.3945.136 YaBrowser/20.2.2.261 Yowser/2.5 Safari/537.36')]
        return br

    def get_foreign_st_list(self):
        station_ids = {}
        url = "http://www.pogodaiklimat.ru/archive.php?id=kz"
        try:
            html = self.br.open(url)
            soup = BeautifulSoup(html, "lxml")
            links = soup.findAll("li", {"class": "big-blue-billet__list_link"})
            for link in links:
                href = link.find('a').get('href')
                station_name = link.find('a').text

                if 'id=' in href:
                    print(f'{station_name} || {href.split("=")[-1]}')
                    station_ids[f'{station_name}'] = href.split('=')[-1]
        except Exception as e:
            print("[!]Critical, could not open page.")
        return station_ids

    def get_station_list(self):
        station_ids = {}
        try:
            for name, url in self.region_list.items():
                if name == 'Эвенкия':
                    name = 'Красноярский край'
                if name == 'Шпицберген':
                    name = 'Мурманская область'
                if name not in station_ids.keys():
                    station_ids[name] = {}

                html = self.br.open(url)
                soup = BeautifulSoup(html, "lxml")
                links = soup.findAll("li", {"class": "big-blue-billet__list_link"})
                for link in links:
                    href = link.find('a').get('href')
                    station_name = link.find('a').text

                    if 'id=' in href:
                        id = href.split("=")[-1]
                        print(f'{name} - {station_name} || {id}')
                        station_ids[name][station_name] = id
        except Exception as e:
            print("[!]Critical, could not open page.", e)
        return station_ids

    def save_station_list(self):
        filename = STATION_LIST_DIR_RU if self.country == 'RU' else STATION_LIST_DIR_KZ
        with open(filename, 'w') as f:
            json.dump(self.station_ids, f, indent=2, ensure_ascii=False)


Finder('RU').save_station_list()