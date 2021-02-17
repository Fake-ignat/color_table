# coding:cp1251
from logic.utils import load_data, create_browser
from mechanize import Browser
from bs4 import BeautifulSoup
from constants import (STATION_LIST_DIR_KZ, STATION_LIST_DIR_RU, ROOT_DIR, USERNAME, PASSWORD)
import re, json, ast


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


class Coordinator():
    def __init__(self):
        # self.regions = load_data('../stations/station_ids full.json')
        # print(self.regions)
        self.br = create_browser()
        #self.login()
        #self.update_regions()

    def get_URL(self, id):
        # return f'http://www.pogodaiklimat.ru/summary/{id}.htm'
        return f'https://time-in.ru/time/{id}'

    def login(self):
        try:
            self.br.open("http://www.pogodaiklimat.ru/login.php")
        except:
            print("[!]Critical, could not open page.")
        self.br.form = list(self.br.forms())[0]
        self.br["username"] = USERNAME
        self.br["password"] = PASSWORD
        self.br.submit()

    def get_city_id(self, name):
        response = self.br.open(f'https://time-in.ru/time?search={name}&ajax=true').get_data()
        data = ast.literal_eval(response.decode("UTF-8"))
        return data[0]["id"] \
            if data \
            else None

    def get_tag_text(self, url, tag):
        html = self.br.open(url)
        soup = BeautifulSoup(html, "lxml")
        h2 = soup.find(tag)
        return h2.text

    def parse_coords(self, text):
        pattern = r'(\d+\.\d+)°[шд]'
        match = re.findall(pattern, text)
        lat = match[0] if match else None
        long = match[1] if match else None
        lat, long = self.convert_coord(map(float, (lat, long)))
        return lat, long

    def convert_coord(self, coords):
        return map(lambda x:
                   round(
                       int(x) + (x - int(x)) / 60,
                       5),
                   coords)

    def updated_station_data(self, station_id, id):
        if id:
            url = self.get_URL(id)
            html = self.br.open(url)
            soup = BeautifulSoup(html, "lxml")
            tbody = soup.find('tbody')
            try:
                trlat, trlong = tbody.find_all('tr')[3:4]
                lat = float(trlat.find_all('td')[1].text())
                long = float(trlong.find_all('td')[1].text())
                # coord = self.parse_coords(text)
                return dict(id=station_id, coord=[lat, long])
            except Exception:
                print(station_id, id)
        else:
            return

    def get_soup(self, id):
        lat, long = None, None
        url = self.get_URL(id)
        html = self.br.open(url)
        soup = BeautifulSoup(html, "lxml")
        table = soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            k, v = row.find_all('td')
            if k == 'Долгота':
                long = float(v.text())
            if k == 'Широта':
                lat = float(v.text())
            print(k, v)
        return lat, long


    def update_regions(self):
        for region, station_data in self.regions.items():
            for station, station_id in station_data.items():
                print(f'{region} - {station}')
                city_id = self.get_city_id(station)
                if city_id:
                    new_data = self.updated_station_data(station_id, city_id)
                    self.regions[region][station] = new_data

    def save_data(self):
        filename = STATION_LIST_DIR_RU
        with open(filename, 'w') as f:
            json.dump(self.regions, f, indent=2, ensure_ascii=False)

    def extract_from_html(self, html):
        print(html)


coo = Coordinator()
id = coo.get_city_id('Киров')
print(coo.get_soup(id))
