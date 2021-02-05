from utils import get_ids, get_rus_ids
from TableLoader import TableLoader
from constants import target_names, kz_target_names, STATION_LIST_DIR_RU, STATION_LIST_DIR_KZ

tl = TableLoader()
for st_id, name in get_rus_ids(target_names, STATION_LIST_DIR_RU):
    tl.load_all(st_id, name)
    tl.save_as_excel(name)

for st_id, name in get_ids(kz_target_names, STATION_LIST_DIR_KZ):
    tl.load_all(st_id, name)
    tl.save_as_excel(name)



