from mechanize import Browser
from bs4 import BeautifulSoup
from urllib.error import URLError
import xlsxwriter as xl
import xlrd, os, json
from tkinter import *
from tkinter import filedialog
import datetime as dt
# import gismeteo_forecast as gm

start_date = dt.date(2019, 9, 1)
date_list = [(start_date + dt.timedelta(days=x)).strftime("%d.%m") for x in range(122)]

root = Tk()
root.title("Скачать метеоархив станции")
root.geometry("350x50")


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

        # save_file_name = filedialog.asksaveasfile(mode='w', defaultextension=".xls", title="Сохранить результаты как",
        #                                           initialfile=f'Метеоархив {station_name} {years[0]}-{years[-1]}', filetypes=(("XLSX", "*.xlsx"), )).name
        wb = xl.Workbook(save_file_name)
        ws_temp = wb.add_worksheet('Температура')
        ws_wind = wb.add_worksheet('Порывы ветра, мс')
        ws_prep = wb.add_worksheet('Осадки, мм')
        ws_snow = wb.add_worksheet('Высота снега, см')
        # Создаем стили ячеек
        merge_format = wb.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        merge_format.set_border(style=1)

        temp_format = wb.add_format({'num_format': '# ##0', 'align': 'center', 'valign': 'vcenter'})
        temp_format.set_border(style=1)

        # пишем шапки таблиц
        for column in range(len(years)):
            ws_temp.write(0, 1 + column, int(years[column]), merge_format)
            ws_wind.write(0, 1 + column, int(years[column]), merge_format)
            ws_prep.write(0, 1 + column, int(years[column]), merge_format)
            ws_snow.write(0, 1 + column, int(years[column]), merge_format)
        ws_temp.write(0, len(years) + 1, "Прогноз", merge_format)
        row = 1
        # пишем первые столбцы
        for day_month in date_list:
            ws_temp.write(row, 0, day_month, merge_format)
            ws_wind.write(row, 0, day_month, merge_format)
            ws_prep.write(row, 0, day_month, merge_format)
            ws_snow.write(row, 0, day_month, merge_format)
            row += 1
        # пишем данные
        col = 1
        for year in years:
            # начинаем запись каждого столбца с 1 строки
            row = 1
            for key_date in enumerate(date_list):
                # берем дату из списка с 01.01 по 31.12 и присоединием текущий год
                gen_date = key_date[1] + '.' + str(year)
                print('Запись данных за ' + gen_date)
                if len(data[0]) and gen_date in data[col-1].keys():
                    # если в data есть наша сгененрированная дата, пишем эти данные
                    ws_temp.write(row, col, data[col-1][gen_date][0], temp_format)
                    ws_wind.write(row, col, data[col-1][gen_date][1], temp_format)
                    ws_prep.write(row, col, data[col-1][gen_date][2], temp_format)
                    ws_snow.write(row, col, data[col-1][gen_date][3], temp_format)
                else:
                    # если в data нет скачанных данных
                    ws_temp.write(row, col, "Н/Д", temp_format)
                    ws_wind.write(row, col, "Н/Д", temp_format)
                    ws_prep.write(row, col, "Н/Д", temp_format)
                    ws_snow.write(row, col, "Н/Д", temp_format)
                row += 1
            col += 1
        print(f'Архив станции {station_name} успешно записан!')

        # загружаем прогноз с gismeteo
        # forecast = gm.get_forcast(gm.search_url_by_name(station_name, br), br)
        # начинаем записывать прогноз с gismeteo
        row = 1
        for key_date in enumerate(date_list):
            # берем дату из списка с 01.01 по 31.12 и присоединием текущий год
            gen_date = key_date[1] + '.' + str(years[-1])
            """
            if gen_date in forecast.keys():
                # если в forecast есть наша сгененрированная дата, пишем эти данные
                ws_temp.write(row, col, forecast[gen_date], temp_format)
                print("Запись прогноза за " + gen_date)
            else:
                # если в forecast нет скачанных данных
                ws_temp.write(row, col, "", temp_format)
                """
            row += 1
        print('Данные станции "' + station_name + '" успешно записаны!')
        wb.close()
    except IndexError as err:
        pass
    except Exception as e:
        pass

def load_data(station_name, station_id, start_year, end_year, username, password, br):
    # Логинимся на "Погода и климат"
    try:
        br.open("http://www.pogodaiklimat.ru/login.php")
    except Exception as e:
        print("[!]Critical, could not open page.")
        # print "\n %s" % (e)
    br.form = list(br.forms())[0]
    br["username"] = username
    br["password"] = password
    br.submit()
    # После авторизации создаем запросы
    years = list(map(str, range(start_year, end_year + 1)))
    # Создаем переменную для названия станции
    # station_name = ''
    # Создаем список, куда будем складывать считанные значения
    data = []
    print(station_name)
    try:
        for y in years:
            print("Чтение данных за " + y + " год")

            html = br.open('http://www.pogodaiklimat.ru/summary.php?m=&y={}&id={}'.format(y, station_id))

            soup = BeautifulSoup(html, "lxml")
            # Находим все строки таблицы с данными
            table_rows = soup.find_all('tr')[2:]
            # создаём словарь для записи с ключом - дата
            c_data = {}
            # проходимся по каждой строке
            for row in table_rows:

                date_cell = row.find_all('td')[2].text
                c_data.setdefault(date_cell, [])

                # получаем все ячейки в строке
                cells = row.find_all('td')

                # if station_name == "":
                #     station_name = cells[1].text

                if len(cells) > 43:
                    date = cells[2].text

                    av_temp = float(cells[3].text) if cells[3].text != '' else 'Н/Д'
                    gust = int(cells[14].text) if cells[14].text != '' else 'Н/Д'
                    sum_prep = float(cells[26].text) if cells[26].text != '' else 'Н/Д'
                    try:
                        max_snow = int(float(cells[27].text))
                    except ValueError:
                        max_snow = ''
                    c_data[date].append(av_temp)
                    c_data[date].append(gust)
                    c_data[date].append(sum_prep)
                    c_data[date].append(max_snow)
                else:
                    continue
            data.append(c_data)

    except URLError as err:
        pass
    except Exception as e:
        pass

    save_data(data, years, station_name, br)


def read_params(name):
    if name != '':
        wb = xlrd.open_workbook(name)
        sheet = wb.sheet_by_index(0)
        vals = [sheet.row_values(n) for n in range(sheet.nrows)]

        station_id = str(int(vals[0][1]))
        start_year = int(vals[2][1])
        end_year = int(vals[4][1])
        username = str(vals[6][1])
        password = str(vals[8][1])

        load_data(station_id, start_year, end_year, username, password, create_Browser())
        wb.close()

def open_file():
    try:
        name_file = filedialog.askopenfile("r", title='Выберите файл с настройками').name
        read_params(name_file)
    except AttributeError:
        pass

def start():
    stations_ids = {}
    # stations_ids = [27612, 26063]
    start_year = 2015
    end_year = 2020
    username, password = 'ncuksods', 'ncuksods'

    filename = f'{os.curdir}/station_ids.json'
    with open(filename, 'r') as f:
        stations_ids = json.load(f)

    for station_name, st_id in stations_ids.items():
        load_data(station_name, st_id, start_year, end_year, username, password, create_Browser())

# button1 = Button(root, text="Выбрать файл с параметрами", command=start)
# button1.pack()
#
# root.mainloop()

start()




