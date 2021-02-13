from os.path import abspath, split, dirname
from datetime import datetime


USERNAME, PASSWORD = ['ncuksods', 'ncuksods']
THIS_YEAR = datetime.now().year

FIRST_YEAR = 2010
LAST_YEAR = 2021

MERGE_FORMAT = {'bold': 1, 'align': 'center', 'valign': 'vcenter'}
TEMP_FORMAT = {'num_format': '# ##0', 'align': 'center', 'valign': 'vcenter'}
PREP_SNOW_FORMAT = {'align': 'center', 'valign': 'vcenter'}

target_names = ['Алдан', 'Амга', 'Белая Гора', 'Усть-Куйга', 'Великий Устюг', 'Ишим', 'Чарышское', 'Зырянка', 'Ленск',
                'Усть-Цильма', 'Черлак']
kz_target_names = ['Петропавловск', 'Кокшетау', 'Рузаевка', 'Павлодар']

this_file_dir = dirname(abspath(__file__))
ROOT_DIR = split(this_file_dir)[0]
STATION_LIST_DIR_RU = f'{ROOT_DIR}/stations/station_ids full.json'
STATION_LIST_DIR_KZ = f'{ROOT_DIR}/stations/kz_station_ids.json'
