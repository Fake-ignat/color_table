import folium
from constants import START_LOC, START_ZOOM
from logic.utils import load_data

filename = "../stations/ru_meteo_locaton.json"


class MyMap:

    def __init__(self):
        self.data = load_data(filename)
        self.map = folium.Map(location=START_LOC, zoom_start=START_ZOOM, dragging=True)

    def add_points(self):
        for name, loc in self.get_names_and_coords():
            point = create_marker(name, loc)
            point.add_to(self.map)

    def get_names_and_coords(self):
        coords = []
        for region, stations in self.data.items():
            for station, vals in stations.items():
                loc = vals["location"]
                if loc:
                    coords.append((station, loc))
        return coords

    def save_map(self, filename):
        self.map.save(filename)


def create_marker(name, loc):
    return folium.CircleMarker(location=loc,
                               popup=f'{name} {loc[0]} {loc[1]}',
                               color='black',
                               fill_color='yellow',
                               fill_opacity=0.9)


my_map = MyMap()
my_map.add_points()
my_map.save_map("map.html")
