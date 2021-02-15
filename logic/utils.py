import json
from mechanize import Browser
from logic.constants import MERGE_FORMAT, TEMP_FORMAT, PREP_SNOW_FORMAT


def create_browser():
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('user-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                    ' Chrome/79.0.3945.136 YaBrowser/20.2.2.261 Yowser/2.5 Safari/537.36')]
    return br


def merge_cells(worksheet, width, height, cell_format, station_name):
    worksheet.merge_range(0, 0, 0, width, station_name, cell_format)
    worksheet.merge_range(2, 0, 2, width, "Среднемесячная температура, °С", cell_format)
    worksheet.merge_range(2 + height, 0, 2 + height, width, "Суммарные осадки, мм", cell_format)
    worksheet.merge_range(2 + 2 * height, 0, 2 + 2 * height, width, "Максимальная высота снега, см", cell_format)


def write_1st_col(worksheet, height, cells_format, month_names):
    for i in range(height - 1):
        for block in range(3):
            line = 3 + i + block * height
            worksheet.write(line, 0, month_names[i], cells_format)


def get_conditional_format(i):
    return {'type': '3_color_scale',
            'min_color': '#6FAE83' if i else '#6C9AD2',
            'mid_color': '#FFFF99' if i else 'white',
            'max_color': '#DB6868'
            }


def apply_conditional_format(worksheet, height, width):
    for row in range(3, 3 + height):
        for block in range(3):
            line = row + block * height
            worksheet.conditional_format(line, 1, line, width, get_conditional_format(block))


def get_ids(st_names, filename):
    ids = []
    for target_name in st_names:
        with open(filename, 'r') as f:
            stations_ids = json.load(f)
            for station_name, st_id in stations_ids.items():
                if target_name in station_name:
                    ids.append((st_id, station_name))
    return ids


def load_data(filename):
    data = {}
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def get_rus_ids(st_names, filename):
    ids = []
    regions = load_data(filename)
    for target_name in st_names:
        # target_region = None
        # if '-' in target_name:
        #     target_region, target_name = map(lambda x: x.strip, target_name.split('-'))
        for region, stations in regions.items():
            # if target_region:
            #     if target_region not in region:
            #         continue
            for station in stations:
                if target_name in station:
                    id = stations[station]
                    ids.append((id, f'{region} - {station}'))
    return ids


def is_start_of_year(date):
    return date.startswith(('01', '1.'))


def to_new_col(col):
        col += 1
        return 3, col


def write_data(worksheet, data, height, formats):
    line = 3
    col = 0
    for month_year, values in data.items():
        if is_start_of_year(month_year):
            line, col = to_new_col(col)

        for i, value in enumerate(values):
            row = line + i * height
            cell_format = formats[1] if i else formats[0]
            worksheet.write(row, col, value, cell_format)
        line += 1


def cell_formats(workbook):
    merge_format = workbook.add_format(MERGE_FORMAT)
    merge_format.set_border(style=1)

    temp_format = workbook.add_format(TEMP_FORMAT)
    temp_format.set_border(style=1)

    prep_snow_format = workbook.add_format(PREP_SNOW_FORMAT)
    prep_snow_format.set_border(style=1)

    return merge_format, temp_format, prep_snow_format


def local_st_name(name):
    return "-".join(name.split("-")[1:])
