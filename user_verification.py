
import email
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import OneLineIconListItem
from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.tab import MDTabsBase
from kivy.uix.scrollview import ScrollView
from kivymd.toast import toast


class UserVerification(Screen):
    user_category = ["Student", "Old Age", "Differently Able", "Others"]
    user_date_of_birth = None
    user_category_name = None
    profile_pic_path = None
    citizenship_path = None
    id_card_path = None
    database_ref = None
    user_key = None
    tab_list = None

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.database_ref = app.realtime_database
        self.user_key = app.user_id
        self.tab_list = self.ids.main_tab.get_tab_list()
        self.ids.address_tab.disabled = True
        self.ids.document_tab.disabled = True

        user_list = [
            {
                "viewclass": "IconListItem",
                # "height": dp(56),
                "text": f'{category}',
                "on_release": lambda x=f'{category}': self.set_user_category(x),
            }
            for category in self.user_category]
        self.user_cat = MDDropdownMenu(
            caller=self.ids.usercategory,
            items=user_list,
            position="center",
            width_mult=56,
            border_margin=5,
        )

        return super().on_pre_enter(*args)

    def set_user_category(self, text__item):
        self.ids.usercategory.text = text__item
        self.user_category_name = text__item
        self.user_cat.dismiss()
        # print(self.user_category_name)

    def pp_file_selection(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.pp_select_path,
            preview=True,
        )
        self.file_manager.show('/')
        self.manager_open = False

    def citizen_file_selection(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.citizen_select_path,
            preview=True,
        )
        self.file_manager.show('/')
        self.manager_open = False

    def id_card_file_selection(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.id_card_select_path,
            preview=True,
        )
        self.file_manager.show('/')
        self.manager_open = False

    def pp_select_path(self, path):
        self.exit_manager()
        self.profile_pic_path = path
        # print(path)
        # toast(path)

    def citizen_select_path(self, path):
        self.exit_manager()
        self.citizenship_path = path
        # print(path)

        # toast(path)

    def id_card_select_path(self, path):
        self.exit_manager()
        self.id_card_path = path
        # print(path)

        # toast(path)
    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.user_date_of_birth = str(value)
        # print(value)
        # pass

    def on_cancel(self, instance, value, date_range):
        pass

    def callback(self):
        self.manager.current = 'userhome'
        self.manager.transition.direction = 'right'

    def store_general_information(self):
        user_name = self.ids.user_name.text
        user_email = self.ids.email_address.text
        print(user_email)

        if (len(user_name) != 0 and len(user_email) != 0 and self.user_date_of_birth != None and self.user_category_name != None):
            print(user_name, self.user_date_of_birth, self.user_category_name)

            self.database_ref.database().child("User Verification").child("General Information").child(self.user_key).set(
                {'UserName': user_name, "E-mail": user_email, "card_validity": self.user_date_of_birth,
                    "User Category": self.user_category_name}
            )

            toast("General Information Registration Sucessfull")
            self.ids.address_tab.disabled = False
            if (self.user_category_name == "Others"):
                print(self.user_category_name)
                self.ids.idcard.disabled = True
            else:
                self.ids.idcard.disabled = False
        # self.ids.document_tab.disabled: 'False'

            self.ids.main_tab.switch_tab(self.tab_list[1])

        else:
            toast("Please enter all credientails")

    def store_address_information(self):
        # self.ids.document_tab.disabled: 'False'
        # self.ids.generalinfo.disabled: 'False'
        permanent_address = self.ids.permanentaddress.text
        province_name = self.ids.province.text
        district_name = self.ids.district.text
        zone_name = self.ids.Zone.text
        municipality = self.ids.Municipality.text
        tole = self.ids.tole.text
        if (len(permanent_address) != 0 and len(province_name) != 0 and len(district_name) != 0 and len(zone_name) != 0 and len(municipality) != 0 and len(tole) != 0):

            print(permanent_address, province_name,
                  district_name, zone_name, municipality, tole)
            self.database_ref.database().child("User Verification").child("Address Information").child(self.user_key).set(
                {"Country ": permanent_address, "Province": province_name, "District": district_name,
                    "Zone": zone_name, "Municipality": municipality, "Tole": tole}
            )
            toast("Address Registration Sucessfull")
            # self.ids.address_tab.disabled: 'False'
            self.ids.document_tab.disabled = False
            self.ids.main_tab.switch_tab(self.tab_list[2])
        else:

            toast("Please enter all credientails")

        # pass
    def store_documents_location(self):

        print(self.user_key)

        if (self.citizenship_path != None or self.profile_pic_path != None):
            print(self.citizenship_path, self.id_card_path, self.profile_pic_path)

            self.profile_pic_path = str(
                self.profile_pic_path).replace("\\", "//")
            self.citizenship_path = str(
                self.citizenship_path).replace("\\", "//")
            self.id_card_path = str(self.id_card_path).replace("\\", "//")

            # print(self.citizenship_path,self.id_card_path,self.profile_pic_path)

            try:

                self.database_ref.storage().child(
                    f'{self.user_key}/profile.jpg').put(self.profile_pic_path)
                self.database_ref.storage().child(
                    f'{self.user_key}/citizenship.jpg').put(self.citizenship_path)
                self.database_ref.storage().child(
                    f'{self.user_key}/identitycard.jpg').put(self.id_card_path)
                toast("Document Uploading Sucessfull")
                self.manager.current = 'userhome'
                self.manager.transition.direction = 'right'
            except:
                toast("Invalid file location")

        else:
            toast("Please select the necessary document")


# class Tabs(MDTabsBase,ScrollView):
#     pass
class IconListItem(OneLineIconListItem):
    icon = StringProperty()
