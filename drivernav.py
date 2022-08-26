from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class DriverNavigation(Screen):
    city_name = None
    route_name = None
    app = App.get_running_app()
    # getting route name from the data base

    database_route_list = app.firestore_database.collection(
        'Kathmandu Bus Route List').get()

    def on_pre_enter(self, *args):
    #     # city name dropdown
    #     # city_items = [
    #     #     {
    #     #         "viewclass": "IconListItem",
    #     #         "text": f"Item {i}",
    #     #         "on_release": lambda x=f"Item {i}": self.set_city_name(x),
    #     #     }
    #     #     for i in range(5)]

    #     # self.city = MDDropdownMenu(
    #     #     caller=self.ids.city_name,
    #     #     items=city_items,
    #     #     position="bottom",
    #     #     width_mult=10,
    #     # )
    #     # route name list
        route_items = [
            {
                "viewclass": "IconListItem",
                "text": f'{route_name.id}',
                "on_release": lambda x=f'{route_name.id}': self.set_route_name(x),
            }
            for route_name in self.database_route_list]
        self.route = MDDropdownMenu(
            caller=self.ids.route_name,
            items=route_items,
            position="bottom",
            width_mult=8,
    
            
        )

        return super().on_pre_enter(*args)

    # def set_city_name(self, text__item):
    #     self.ids.city_name.text = text__item
    #     self.city_name=text__item
    #     self.city.dismiss()
        # print(self.city_name)
    # set route name in dropdown
    def set_route_name(self, text__item):
        self.ids.route_name.text = text__item
        self.route_name = text__item
        self.route.dismiss()
        # print(self.route_name)

    def driver_database(self):
        association_name = self.ids.association_name.text
        bus_number = self.ids.bus_number.text
        key = ['association_name', 'route_list']
        values = [association_name, self.route_name]
        driver_dict = {}
        for i in range(len(key)):
            driver_dict[key[i]] = values[i]

        try:
            if (len(association_name) == 0 or len(bus_number) == 0 or len(self.route_name) == 0):
                cancel_btn_username_dialogue = MDFlatButton(
                    text='Retry', on_release=self.close_dilougebox)
                self.dialog = MDDialog(title="Notification", text="Enter all the Details", size_hint=(
                    0.7, 0.2), buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
            else:
                self.app.firestore_database.collection(f'Bus Details').document(
                    f'{bus_number}').set(driver_dict, merge=True)
                self.manager.current = 'userlogin'
                self.manager.transition.direction = 'left'
        except:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Retry', on_release=self.close_dilougebox)
            self.dialog = MDDialog(title="Notification", text="Enter all the Details", size_hint=(
                0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

    def close_dilougebox(self, obj):
        self.dialog.dismiss()

        # print(association_name,bus_number)
        # print(self.route_name,self.city_name)


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
