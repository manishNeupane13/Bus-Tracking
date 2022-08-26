from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from locationinfo import get_lat_and_lon



class RouteDetails(Screen):
    database_ref = None
    route_name = None
    list_of_widgets_added = []

    def on_pre_enter(self, *args):

        app = App.get_running_app()
        self.database_ref = app.realtime_database
        real_data = self.database_ref.database().child(
            "Kathmandu Bus Route Details").get()
        # for i in real_data.each():
        #     print(i.key())
        route_items = [
            {
                "viewclass": "IconListItem",
                "icon": "search-web",
                "text": f'{route_name.key()}',
                "on_release": lambda x=f'{route_name.key()}': self.set_route_name(x),
            }
            for route_name in real_data.each()
        ]

        self.route_menu = MDDropdownMenu(
            caller=self.ids.mainroute,
            items=route_items,
            position="center",
            width_mult=56,
            border_margin=5,
        )

        return super().on_pre_enter(*args)

    def set_route_name(self, text__item):
        global route_name
        self.ids.mainroute.text = text__item
        self.route_name = text__item
        # print(self.route_name)
        self.get_stand_information()

        self.route_menu.dismiss()

    def callback(self):
        self.manager.current = 'userhome'
        self.manager.transition.direction = 'right'

    def get_stand_information(self):
        route_information = self.database_ref.database().child(
            "Kathmandu Bus Route Details").child(self.route_name).get()
        for data in route_information.each():
            # print(data.key(), data.val())
            new_widget = (OneLineAvatarIconListItem(text=f'{data.val()}'))
            self.list_of_widgets_added.append(new_widget)
            self.ids.listitem.add_widget(new_widget)

        

    def remove_widget(self):
        for i in range(len(self.list_of_widgets_added)):
            self.ids.listitem.remove_widget(self.list_of_widgets_added[i])


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
