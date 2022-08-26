
from datetime import datetime
from kivy.garden.mapview import MapMarker
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivymd.toast import toast
import webbrowser 
import socket
hostname = socket.gethostname()
# get ip address
ip_address = socket.gethostbyname(hostname)
port = 9000


from locationinfo import get_location_name, get_distance_travelled
from paymentinfo import get_fare_amount


class BusMarker(MapMarker):

    def close_dilougebox(self, obj):
        self.dialog.dismiss()

    def payment_dilougebox_close(self, obj):
        self.payment_dialog.dismiss()

    def on_release(self):
        cancel_btn_username_dialogue = MDFlatButton(
            text='Close', on_release=self.close_dilougebox)
        payment_section = MDFlatButton(
            text='Accept', on_release=self.open_epay)
        self.dialog = MDDialog(title="PAYMENT", type="custom", auto_dismiss=False, content_cls=Content(self.lat, self.lon), size_hint=(
            1, 1), buttons=[cancel_btn_username_dialogue])
        self.dialog.open()

    # def payment_details(self, obj):
    #     cancel_btn_username_dialogue = MDFlatButton(
    #         text='Cancel', on_release=self.payment_dilougebox_close)
    #     proceed_payment = MDFlatButton(
    #         text='Proceed', on_release=self.open_epay)
    #     self.payment_dialog = MDDialog(title="Payment Details", type="custom", content_cls=Content(), size_hint=(
    #         0.7, 0.2), buttons=[cancel_btn_username_dialogue, proceed_payment])
    #     self.payment_dialog.open()

    def open_epay(self, obj):

        pass


class Content(BoxLayout):
    # route_name = None

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
        super().__init__()
        #print(self.latitude, self.longitude)

        self.inital_location = get_location_name(self.latitude, self.longitude)
        print(self.inital_location.split(',')[0])
        self.fareamount = None
        self.distance_travelled = None
        self.final_stand_name = None
        self.ids.farecost.text = f'Fare Amount'

        self.app = App.get_running_app()
        self.database_ref = self.app.realtime_database
        self.user_key = self.app.user_id

        user_information = self.database_ref.database().child(
            "User Verification").child("General Information").child(self.user_key).get()
        for data in user_information.each():
            if data.key() == "User Category":
                self.user_cateogry = data.val()
                break
                # print(data.val())
        real_data = self.database_ref.database().child(
            "Real Tiime Location Data").get()
        for i in real_data.each():
            for j in (i.val().values()):
                # print("ke", i.key())
                # print("Route", j['Route_Name'])
                # print("own", self.latitude, self.longitude)
                # print((str(self.latitude))[0:5], (str(self.longitude))[0:5])
                # print((str(j['Latitude'])[0:5]), (str(j['Longitude'])[0:5]))
                # print("database", j['Longitude'], j['Latitude'])
                if str(self.latitude)[0:5] == str(j['Latitude'])[0:5] and str(self.longitude)[0:5] == str(j['Longitude'])[0:5]:
                    # print("condition sucess")
                    # print("ke", i.key())
                    self.driver_number = i.key()
                    self.route_name = j['Route_Name']
                    # print("Route", j['Route_Name'])
                    break
        self.ids.initiallocation.text = f'{self.inital_location.split(",")[0]}'
        self.ids.user_category.text = f'User Category\n{self.user_cateogry}'
        try:
            self.bus_stand_data = self.database_ref.database().child(
                "Kathmandu Bus Route Details").child(self.route_name).get()
        except:
            toast("Bus Stand Data Fetching Unsucessfull")

        stop_name = [
            {
                "viewclass": "IconListItem",
                "icon": "search-web",
                "text": f'{stand_name.val()}',
                "on_release": lambda x=f'{stand_name.val()}': self.set_route_name(x),
            }
            for stand_name in self.bus_stand_data.each()]

        self.app.menu = MDDropdownMenu(
            caller=self.ids.finalstop,
            items=stop_name,
            position="center",
            width_mult=56,
            border_margin=5,
        )

    def set_route_name(self, text__item):
        self.ids.finalstop.text = text__item
        self.final_stand_name = text__item
        try:

            self.distance_travelled = (get_distance_travelled(
                self.inital_location.split(",")[0], self.final_stand_name))
        except:
            toast("Distance Travelled Not Found")
        self.fareamount = get_fare_amount(
            self.user_cateogry, self.distance_travelled)
        self.ids.farecost.text = f'Fare Amount\nRs{self.fareamount}'
        self.send_fare_amount(self.fareamount)
        self.app.menu.dismiss()

    def payment_access(self):
        id = str(datetime.now())
        try:
            self.database_ref.database().child("Payment Details").child("Service User").child(self.user_key).set(
                {"Payment ID": str(id), "Reciver": str(self.driver_number), "Initial Location": str(self.inital_location.split(",")[0]), "Final Destination ": str(self.final_stand_name), 'Distance Travelled': str(self.distance_travelled), 'Amount Paid ': str(self.fareamount)})
            self.database_ref.database().child("Payment Details").child(
                "Service Provider").child(self.driver_number).set({"Payment ID": str(id), "Sender": str(self.user_key), "Sender Category": str(self.user_cateogry), "Initial Location": str(self.inital_location.split(",")[0]), "Final Destination ": str(self.final_stand_name), 'Distance Travelled': str(self.distance_travelled), 'Amount Paid ': str(self.fareamount)})
            toast("Payment Sucessfull")
            webbrowser.open_new_tab(f'http://{ip_address}:{port}/{self.fareamount}')
            
           
        except:
            toast("Payment Unsucessfull")
    def send_fare_amount(self,amount):
        return amount

        # print(self.inital_location, self.final_stand_name,
        #       self.user_cateogry, self.distance_travelled, self.fareamount)
        # print(self.user_key, self.driver_number)


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
