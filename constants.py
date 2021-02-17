from os.path import abspath, split, dirname
from datetime import datetime

# данные для аутентификации на сайте
USERNAME, PASSWORD = ['ncuksods', 'ncuksods']

# получаем значение этого года
THIS_YEAR = datetime.now().year

# форматы для редактирования excel
MERGE_FORMAT = {'bold': 1, 'align': 'center', 'valign': 'vcenter'}
TEMP_FORMAT = {'num_format': '# ##0', 'align': 'center', 'valign': 'vcenter'}
PREP_SNOW_FORMAT = {'align': 'center', 'valign': 'vcenter'}

# получаем абсолютный путь к корневой директории
ROOT_DIR = dirname(abspath(__file__))

# путь к файлам со всеми станциями
STATION_LIST_DIR_RU = f'{ROOT_DIR}/stations/station_ids full.json'
STATION_LIST_DIR_KZ = f'{ROOT_DIR}/stations/kz_station_ids.json'

# для внешнего вида графического интерфейса
BG_COLOR = '#3e3e3e;'
WIDGET_STYLE = f'background-color: {BG_COLOR};'

BTN_COLOR = "#e3e3d4"
CHECKED_COLOR = "#ffaa7f"
SPIN_COLOR = "#e3e3d4"
CB_COLOR = "#e3e3d4"

# для отрисовки карты
START_LOC = [55.75, 37.6167]
START_ZOOM = 7
