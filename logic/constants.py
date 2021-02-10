import os

# MONTHS = ["ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ", "ИЮНЬ",
#           "ИЮЛЬ", "АВГУСТ", "СЕНТЯБРЬ", "ОКТЯБРЬ", "НОЯБРЬ", "ДЕКАБРЬ"]
#
# DEFAULT_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

MONTHS = ["ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ",  "НОЯБРЬ", "ДЕКАБРЬ"]

DEFAULT_MONTHS = [1, 2, 3, 4, 5, 11, 12]


USERNAME, PASSWORD = ['ncuksods', 'ncuksods']

# ToDo получить этот год программно
THIS_YEAR = 2021

FIRST_YEAR = 2010
LAST_YEAR = 2021


MERGE_FORMAT = {'bold': 1, 'align': 'center', 'valign': 'vcenter'}
TEMP_FORMAT = {'num_format': '# ##0', 'align': 'center', 'valign': 'vcenter'}
PREP_SNOW_FORMAT = {'align': 'center', 'valign': 'vcenter'}

# target_names = ['Чарышское']
target_names = ['Алдан', 'Амга', 'Белая Гора', 'Усть-Куйга', 'Великий Устюг', 'Ишим', 'Чарышское', 'Зырянка', 'Ленск',
                'Усть-Цильма', 'Черлак']

# kz_target_names = ['Петропавловск', 'Кокшетау', 'Рузаевка', 'Павлодар']
kz_target_names = ['Рузаевка']

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATION_LIST_DIR_RU = f'{ROOT_DIR}/stations/station_ids full.json'
STATION_LIST_DIR_KZ = f'{ROOT_DIR}/stations/kz_station_ids.json'