from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image
# from kivymd.uix.fitimage import FitImage


class UserHome(Screen):
    database_ref = None
    user_key = None
    # user_information_data=None
    user_name = None

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.database_ref = app.realtime_database
        # print(self.database_ref.database())
        self.user_key = app.user_id
        # print(self.user_key)
        values = []
        try:
            user_information_data = self.database_ref.database().child(
                "User Verification").child("General Information").child(self.user_key).get()

            for i in user_information_data.each():
                values.append(i.val())

            self.user_name = values[2]

            # print(values[2],values[1])

            try:
                self.ids.usernamelbl.text = values[2]
                self.ids.usercategorylbl.text = values[1]
                self.ids.verification_badge.source='images//icons//verified.ico'
            except:
                print("Label not update")

            try:
                self.database_ref.storage().child(
                    f'{self.user_key}/profile.jpg').download("images/UserImage/profile.jpg")
                self.ids.ProfileImg.source = 'images/UserImage/profile.jpg'

            except:
                print("Profile Picture Addition Not SucessFull")
                pass

        except:
            toast("Please verify your kyc")

        return super().on_pre_enter(*args)

    def user_information_screen(self):
        if (self.user_name != None):
            self.manager.current = 'verifieduser'
            self.manager.transition.direction = 'right'
            pass
        else:
            self.manager.current = 'userverify'
            self.manager.transition.direction = 'right'
            pass
