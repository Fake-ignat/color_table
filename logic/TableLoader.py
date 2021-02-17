import xlsxwriter as xl
import statistics as stat
import excel2img
import os
from bs4 import BeautifulSoup
from constants import THIS_YEAR, USERNAME, PASSWORD, ROOT_DIR
from logic.utils import create_browser, merge_cells, write_1st_col, apply_conditional_format, \
    cell_formats, write_data, local_st_name


class TableLoader:
    url = "http://www.pogodaiklimat.ru/msummary.php?m=all"

    def __init__(self, holder):
        self.holder = holder

        self.start_year = self.holder.start_year()
        self.end_year = self.holder.end_year()
        self.years = self.get_years_range()

        self.month_nums = self.holder.chosen_month_nums()
        self.month_names = self.holder.chosen_month_names()

        self.data = self.create_default_buffer()

        self.br = create_browser()
        self.login()

    def create_default_buffer(self):
        buffer = {}
        for year in self.years:
            for month in self.month_nums:
                m_y_date = f'{month:02d}.{year}'
                buffer[m_y_date] = ("Н/Д", "Н/Д", "Н/Д")
        return buffer

    def get_years_range(self):
        return range(self.start_year, self.end_year + 1)

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
                if month in self.month_nums:
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

    def load_all(self, station_name, station_id):
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

        years_text = f'{self.start_year}-{self.end_year}' \
            if self.start_year != self.end_year \
            else f'{self.start_year}'

        # создаем книгу Excel
        workbook_name = f'{ROOT_DIR}/Таблицы/Цветная таблица {st_name} {years_text}'
        worksheet_name = 'Средние показатели'
        wb = xl.Workbook(workbook_name + '.xlsx')
        ws = wb.add_worksheet(worksheet_name)

        # задаем форматы
        formats = cell_formats(wb)

        table_width = len(self.years)
        block_height = len(self.month_names) + 1

        # делаем объединенные ячейки
        merge_cells(ws, table_width, block_height, formats[0], st_name)

        # пишем первый столбец
        write_1st_col(ws, block_height, formats[0], self.month_names)

        # пишем строчку с годами
        for i in range(table_width):
            ws.write(1, 1 + i, int(self.years[i]), formats[0])

        # пишем данные
        write_data(ws, self.data, block_height, formats[1:])

        # условное форматирование
        apply_conditional_format(ws, block_height, table_width)

        # закрываем книгу Excel
        wb.close()

        lst_name = local_st_name(st_name)

        try:
            make_xlsx_screenshot(workbook_name, worksheet_name, lst_name)
        except Exception as e:
            print(e)

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


def make_xlsx_screenshot(wb_name, ws_name, st_name):
    if not os.path.exists('Скриншоты'):
        os.mkdir('Скриншоты')
    screenshot_name = f'{ROOT_DIR}/Скриншоты/{st_name}.png'
    excel2img.export_img(f"{wb_name}.xlsx", screenshot_name, ws_name, None)