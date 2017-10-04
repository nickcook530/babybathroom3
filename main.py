import kivy
import requests
from requests.auth import HTTPBasicAuth
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.garden.mapview import MapView, MapMarker, MapLayer, MarkerMapLayer, Coordinate, MapSource

__version__ = "0.01"

class CustomMapMarker(MapMarker):
    def __init__(self, name, description, *args, **kwargs):
        self.name = name
        self.description = description
        super().__init__(*args, **kwargs)


class CustomMapView(MapView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.mark_me()
        self.mark_boys()
        self.mark_girls()

    def mark_me(self):
        # mark user location and centers map on it
        my_name, my_description, my_lon, my_lat = find_me()
        m1 = CustomMapMarker(lon=my_lon, lat=my_lat, name=my_name, description=my_description, source=r'C:\Users\ncook\Program\learnkivy\start_flag.png')
        m1.bind(on_press = pop_that)
        self.add_marker(m1)
        self.center_on(my_lat, my_lon)


    def mark_boys(self):
        #
        boy = MarkerMapLayer()
        self.add_layer(boy)

        longitude = -71.979914
        latitude = 41.800495
        m1 = MapMarker(lon=longitude, lat=latitude, source=r'C:\Users\ncook\Program\learnkivy\blue_pin.png')
        m1.bind(on_press=pop_that)
        self.add_marker(m1, layer=boy)


    def mark_girls(self):
        # used to draw in all girl's changing rooms
        # change icon to pink
        girl = MarkerMapLayer()
        self.add_layer(girl)

        longitude = -72.979914
        latitude = 40.800495
        m1 = MapMarker(lon=longitude, lat=latitude, source=r'C:\Users\ncook\Program\learnkivy\pink_pin.png')
        m1.bind(on_press=pop_that)
        self.add_marker(m1, layer=girl)

def pop_that(event):
    popup = Popup(title=str(event.name),
                  content=Label(text=str(event.description)),
                  size_hint=(.3, .3))
    popup.open()

def find_me():
    #find user location using plyer, temporary spoof
    #my_lon = -72.979914
    #my_lat = 41.800495
    #my_coord = (my_lon, my_lat)
    #squery_dict = {}
    with requests.Session() as s:
        query_dict = s.get('http://nickcook530.pythonanywhere.com/bloc', auth=HTTPBasicAuth('babykivy', 'knockknock469')).json()
        s.close()
    my_info = (query_dict['1']['name'], query_dict['1']['description'], query_dict['1']['lon'], query_dict['1']['lat'])
    return my_info


class MainApp(App):
    def build(self):
        map = CustomMapView(zoom=16)
        map.map_source = MapSource(min_zoom=10)
        #map.mark_me()
        #map.mark_boys()
        #map.mark_girls()
        return map

if __name__ == '__main__':
    MainApp().run()
