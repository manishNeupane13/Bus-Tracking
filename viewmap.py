from kivy.garden.mapview import MapView
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.garden.mapview import MapMarkerPopup
from busmarker import BusMarker
from database_conn import realtime_db_connection

route_name = ""
real_data = None


class MapBusView(Screen):
    global route_name
    getting_markets_timer = None
    # store information form firebase realtime data base
    BusDetails = []
    # variable to store route selected
    # getting route name from the data base
    bus_location_widget_list = []

    database_route_list = realtime_db_connection().database().child(
        "Kathmandu Bus Route Details").get()

    # putting route name list inside the menus from data base

    def on_pre_enter(self, *args):
        global real_data
        real_data = realtime_db_connection().database().child(
            "Real Tiime Location Data").child().get()
        route_items = [
            {
                "viewclass": "IconListItem",
                "icon": "search-web",
                "text": f'{route_name.key()}',
                "on_release": lambda x=f'{route_name.key()}': self.set_route_name(x),
            }
            for route_name in self.database_route_list.each()]

        self.route_menu = MDDropdownMenu(
            caller=self.ids.routename,
            items=route_items,
            position="center",
            width_mult=56,
            border_margin=5,
        )

        return super().on_pre_enter(*args)
    # setting the route name in the textfield

    def set_route_name(self, text__item):
        global route_name
        self.ids.routename.text = text__item
        route_name = text__item
        self.get_bus_live_location()
        self.route_menu.dismiss()
        # print("set",route_name)

    def get_bus_live_location(self):
        global route_name
        global real_data
        for x in real_data.each():
            for val in x.val().values():
                if route_name == val['Route_Name']:
                    # print(x.val().keys())
                    self.add_bus_live_location(
                        val['Latitude'], val['Longitude'])
                    break

    def add_bus_live_location(self, latitude, longitude):

        # Create the MarketMarker
        # print(latitude, longitude)
        bus_location_marker_widget = BusMarker(
            source="images//icons//bus.ico", lat=latitude, lon=longitude)
        # bus_location_marker_widget = MapMarkerPopup(source="images//icons//bus.ico", lat=latitude, lon=longitude)
        # source="images//icons//bus.ico", lat=latitude, lon=longitude)

        self.bus_location_widget_list.append(bus_location_marker_widget)
        self.ids.viewlocation.add_marker(bus_location_marker_widget)
        # self.remove_marker(MapMarkerPopup())
        # bus_marker = BusMarker(
        #     source="images//icons//bus.ico", lat=latitude, lon=longitude)

        # self.add_marker(bus_marker)
    def remove_location_marker(self):
        for i in range(len(self.bus_location_widget_list)):
            self.ids.viewlocation.remove_marker(
                self.bus_location_widget_list[i])
        pass

    def open_payment_dialog(self):
        pass

    def callback(self):
        self.manager.current = 'userhome'
        self.manager.transition.direction = 'right'


class LocationView(MapView):
    getting_markets_timer = None
    market_names = []

    def start_getting_markets_in_fov(self):
        # After one second, get the markets in the field of view
        try:
            self.getting_markets_timer.cancel()
        except:
            pass

        self.getting_markets_timer = Clock.schedule_once(
            self.get_markets_in_fov, 1)

    def get_markets_in_fov(self, *args):
        global route_name
        global real_data
        for x in real_data.each():

            for val in x.val().values():
                if route_name == val['Route_Name']:
                    self.add_bus_live_location(
                        val['Latitude'], val['Longitude'])
                    break

        # self.add_bus_live_location(location_list)

    def add_bus_live_location(self, latitude, longitude):

        # Create the MarketMarker
        print(latitude, longitude)
        dummy_marker = MapMarkerPopup(
            source="images//icons//bus.ico", lat=latitude, lon=longitude)
        # self.remove_marker(MapMarkerPopup())

        # bus_marker = BusMarker(
        #     source="images//icons//bus.ico", lat=latitude, lon=longitude)

        # self.add_marker(bus_marker)
        self.add_marker(dummy_marker)

        # self.add_widget(bus_marker)


class IconListItem(OneLineIconListItem):
    icon = StringProperty()