from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.toast import toast
from kivy.uix.image import Image


class VerifiedUser(Screen):
    database_ref = None
    user_key = None

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.database_ref = app.realtime_database
        self.user_key = app.user_id
        keys = []
        values = []
        try:
            user_address_info = self.database_ref.database().child(
                "User Verification").child("Address Information").child(self.user_key).get()
            for i in user_address_info.each():
                keys.append(i.key())
                values.append(i.val())

            # lable for address

            self.ids.Countrylbl.text = keys[0]
            self.ids.Districtlbl.text = keys[1]
            self.ids.Municipalitylbl.text = keys[2]
            self.ids.Provincelbl.text = keys[3]
            self.ids.Tolelbl.text = keys[4]
            self.ids.Zonelbl.text = keys[5]
            # value of save information

            self.ids.Country.text = values[0]
            self.ids.District.text = values[1]
            self.ids.Municipality.text = values[2]
            self.ids.Province.text = values[3]
            self.ids.Tole.text = values[4]
            self.ids.Zone.text = values[5]
        except:
            print("No Value Found")

        try:
            self.database_ref.storage().child(
                f'{self.user_key}/citizenship.jpg').download("images/UserImage/citizenship.jpg")
            self.database_ref.storage().child(
                f'{self.user_key}/identitycard.jpg').download("images/UserImage/identitycard.jpg")
            # self.ids.Citizenship.add_widget(Image(

            # ))
            self.ids.citizenimage.source = 'images//UserImage//citizenship.jpg'
            try:
                self.ids.idcardimg.source = 'images/UserImage/identitycard.jpg'
            except:
                self.ids.idcardimg.soirce = 'images//logo//new_logo.png'

        except:
            print("Picture not downloaded")

        return super().on_pre_enter(*args)

    def callback(self):
        self.manager.current = 'userhome'
        self.manager.transition.direction = 'right'
