from mechanize import Browser
from bs4 import BeautifulSoup
from urllib.error import URLError
import xlsxwriter as xl
import os, json
import datetime as dt

import dropbox

dbx = dropbox.Dropbox('sl.Andv3zGIKf7mxG-yeIRAqV8js_oi7hHT8ajr-R8_azlKbgy6fEg7uIsDjnv3hSbYOZ-yAXkZbXwbmSJkXXenxPAH2MLx1BqIazXXipWNUihnENaJZ-4JJPW0DsjfhAJ9IrFN8bU') # наш access token

def load_to_dropbox(filename, station_name):
    with open(filename,'rb') as file: # открываем файл в режиме чтение побайтово
        response = dbx.files_upload(file.read(), station_name) # загружаем файл: первый аргумент (file.read()) - какой файл; второй - название, которое будет присвоено файлу уже на дропбоксе.
        print(response) # выводим результат загрузки

start_date = dt.date(2015, 1, 1)
date_list = [(start_date + dt.timedelta(days=x)).strftime("%d.%m") for x in range(365)]
existing_files = os.listdir(f'{os.curdir}/Россия/')

def create_Browser():
    # Создаем браузер и настраиваем
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('user-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                    ' Chrome/79.0.3945.136 YaBrowser/20.2.2.261 Yowser/2.5 Safari/537.36')]
    return br


def save_data(data, years, station_name, br):
    try:
        save_file_name =f'{os.curdir}/Россия/Метеоархив {station_name} {years[0]}-{years[-1]}.xlsx'

        wb = xl.Workbook(save_file_name)
        ws = wb.add_worksheet(station_name.split("-")[-1].strip())

        # Создаем стили ячеек
        merge_format = wb.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        merge_format.set_border(style=1)

        temp_format = wb.add_format({'num_format': '# ##0', 'align': 'center', 'valign': 'vcenter'})
        temp_format.set_border(style=1)

        # пишем шапки таблиц
        ws.write(0, 0, "Дата", merge_format)
        ws.write(0, 1, 'Температура', merge_format)
        ws.write(0, 2, 'Порывы ветра, м/с', merge_format)
        ws.write(0, 3, 'Осадки, мм', merge_format)
        ws.write(0, 4, 'Высота снега, см', merge_format)
        ws.write(0, 5, 'Атм. давление, гПа', merge_format)
        row = 1
        # пишем первые столбцы
        for date, params in data.items():
            try:
                temp, gust, prep, snow, pressure = params
                ws.write(row, 0, date, temp_format)
                ws.write(row, 1, temp, temp_format)
                ws.write(row, 2, gust, temp_format)
                ws.write(row, 3, prep, temp_format)
                ws.write(row, 4, snow, temp_format)
                ws.write(row, 5, pressure, temp_format)
            except Exception:
                print(date, len(params), params)
            row += 1
        print(f'Архив станции {station_name} успешно записан!')

        wb.close()
    except IndexError as err:
        print(err)
    except Exception as e:
        print(e)

def load_data(station_name, station_id, start_year, end_year, username, password, br):
    # Логинимся на "Погода и климат"
    try:
        br.open("http://www.pogodaiklimat.ru/login.php")

    except URLError as err:
        print(err)
    except Exception as e:
        print("[!]Critical, could not open page.")

    br.form = list(br.forms())[0]
    br["username"] = username
    br["password"] = password
    br.submit()
    # После авторизации создаем запросы
    years = list(map(str, range(start_year, end_year + 1)))
    # Создаем переменную для названия станции
    # station_name = ''
    # Создаем список, куда будем складывать считанные значения
    data = {}

    print(station_name)
    try:
        for y in years:
            print("Чтение данных за " + y + " год")

            html = br.open('http://www.pogodaiklimat.ru/summary.php?m=&y={}&id={}'.format(y, station_id))

            soup = BeautifulSoup(html, "lxml")
            # Находим все строки таблицы с данными
            table_rows = soup.find_all('tr')[2:]
            # проходимся по каждой строке
            for row in table_rows:

                date_cell = row.find_all('td')[2].text
                data.setdefault(date_cell, [])

                # получаем все ячейки в строке
                cells = row.find_all('td')

                # if station_name == "":
                #     station_name = cells[1].text

                if len(cells) > 43:
                    date = cells[2].text
                    av_temp = float(cells[3].text) if cells[3].text != '' else 'Н/Д'
                    gust = int(cells[14].text) if cells[14].text != '' else 'Н/Д'
                    sum_prep = float(cells[26].text) if cells[26].text != '' else 'Н/Д'
                    pressure = float(cells[16].text) if cells[16].text != '' else 'Н/Д'
                    try:
                        max_snow = int(float(cells[27].text))
                    except ValueError:
                        max_snow = ''
                    params = [av_temp, gust, sum_prep, max_snow, pressure]
                    data[date] = params
                else:
                    continue

    except URLError as err:
        pass
    except Exception as e:
        pass

    save_data(data, years, station_name, br)


def start(region):
    stations_ids = {}
    # stations_ids = [27612, 26063]
    start_year = 2020
    end_year = 2021
    username, password = 'ncuksods', 'ncuksods'

    filename = f'{os.curdir}/station_ids full.json'
    with open(filename, 'r') as f:
        stations_ids = json.load(f)

    # state = 0
    for station_name, st_id in stations_ids.items():
        if region in station_name:
            if not is_existing(station_name):
                # if state-3:
                load_data(station_name, st_id, start_year, end_year, username, password, create_Browser())
                # state += 1
                # else:
                #     return

def is_existing(name):
    # result = list(map(lambda x: x.startswith(f'Метеоархив {name}'), existing_files))
    result = list(map(lambda x: name in x, existing_files))
    return any(result)

def start_many(stations):
    for station in stations:
        start(station)


# start_many()




