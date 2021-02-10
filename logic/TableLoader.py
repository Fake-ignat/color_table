import xlsxwriter as xl
import statistics as stat
import os
from bs4 import BeautifulSoup
from logic.constants import THIS_YEAR, FIRST_YEAR, LAST_YEAR, DEFAULT_MONTHS, MONTHS, USERNAME, PASSWORD
from logic.utils import create_default_buffer, create_browser, merge_cells, write_1st_col, apply_conditional_format, \
    cell_formats, write_data


class TableLoader:
    url = "http://www.pogodaiklimat.ru/msummary.php?m=all"

    def __init__(self, months=None):
        self.br = create_browser()
        self.login()
        # self.stations_ids_and_names = stations_ids_and_names
        self.years = range(FIRST_YEAR, LAST_YEAR + 1)
        if months is None:
            self.months = DEFAULT_MONTHS

        self.years = range(FIRST_YEAR, LAST_YEAR + 1)
        self.data = create_default_buffer(self.years)

    def login(self):
        try:
            self.br.open("http://www.pogodaiklimat.ru/login.php")
        except:
            print("[!]Critical, could not open page.")
        self.br.form = list(self.br.forms())[0]
        self.br["username"] = USERNAME
        self.br["password"] = PASSWORD
        self.br.submit()

    def this_month_data(self, station_id):
        url = f'http://www.pogodaiklimat.ru/summary/{station_id}.htm'
        try:
            html = self.br.open(url)
            soup = BeautifulSoup(html, "lxml")
            table_rows = soup.find_all('tr')[2:]
            date = table_rows[0].find_all('td')[2].text[3:]
        except:
            print("[!]Critical, could not open page.")
            return None, None

        temps, preps, snow_height = [], [], []

        for row in table_rows:
            cells = row.find_all('td')
            if len(cells) > 43:
                if cells[3].text != '':
                    temps.append(float(cells[3].text))

                if cells[26].text != '':
                    preps.append(float(cells[26].text))

                if cells[27].text:
                    try:
                        snow_height.append(int(float(cells[27].text)))
                    except ValueError:
                        pass

        t = round(stat.mean(temps), 1) if temps else 'Н/Д'
        p = int(sum(preps)) if preps else 0

        h = max(snow_height) if snow_height else 'Н/Д'

        return date, (t, p, h)

    def get_soup(self, year, station_id, station_name):
        html = ''
        try:
            html = self.br.open(f'{TableLoader.url}&y={year}&id={station_id}')
        except Exception as e:
            print(e)

        print(f'Загрузка данных станции {station_name} за {year} год')
        return BeautifulSoup(html, "lxml")

    def extract_from_html(self, soup):
        table_rows = soup.find_all('tr')[2:]

        if len(table_rows) > 0:
            for i in table_rows:
                collumns = i.find_all('td')
                m_y_date = collumns[2].text
                month = int(m_y_date.split('.')[0])
                if month in self.months:
                    try:
                        av_temp = float(collumns[3].text)
                    except ValueError:
                        av_temp = "Н/Д"
                    try:
                        sum_prep = float(collumns[26].text)
                    except ValueError:
                        sum_prep = "Н/Д"
                    try:
                        max_snow = collumns[30].text
                        max_snow = 0 if max_snow == '' else int(float(max_snow))
                    except ValueError:
                        max_snow = "Н/Д"

                    self.data[m_y_date] = (av_temp, sum_prep, max_snow)

    def load_all(self, station_id, station_name):
        for y in self.years:
            if y > THIS_YEAR:
                continue
            soup = self.get_soup(y, station_id, station_name)
            self.extract_from_html(soup)

        cur_month_year, values = self.this_month_data(station_id)
        if cur_month_year and values:
            self.data[cur_month_year] = values

    def save_as_excel(self, st_name):
        if not os.path.exists('Таблицы'):
            os.mkdir('Таблицы')
        # создаем книгу Excel
        wb = xl.Workbook(f'Таблицы/Цветная таблица {st_name} {FIRST_YEAR}-{LAST_YEAR}.xlsx')
        ws = wb.add_worksheet('Средние показатели')

        # задаем форматы
        formats = cell_formats(wb)

        table_width = len(self.years)
        block_height = len(MONTHS) + 1

        # делаем объединенные ячейки
        merge_cells(ws, table_width, block_height, formats[0], st_name)

        # пишем первый столбец
        write_1st_col(ws, block_height, formats[0])

        # пишем строчку с годами
        for i in range(table_width):
            ws.write(1, 1 + i, int(self.years[i]), formats[0])

        # пишем данные
        write_data(ws, self.data, block_height, formats[1:])

        # условное форматирование
        apply_conditional_format(ws, block_height, table_width)

        # закрываем книгу Excel
        wb.close()

    def print_data(self):
        for d, values in self.data.items():
            t, p, h = values
            m, y = map(int, d.split('.'))
            print(f'{m:02d}.{y} {t} {p} {h}\n')

    def to_TXT(self, name):
        with open(f'data {name}.txt', 'w') as f:
            for d, values in self.data.items():
                t, p, h = values
                m, y = map(int, d.split('.'))
                f.write(f'{m:02d}.{y} {t} {p} {h}\n')

