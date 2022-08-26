from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from database_conn import realtime_db_connection
from database_conn import firestore_db_connection

# Window.size = 385, 700


class WelcomeScreen(Screen):
    pass


class BusTracking(MDApp):

    def build(self):
        self.realtime_database = realtime_db_connection()
        self.firestore_database = firestore_db_connection()
        self.theme_cls.primary_palette = "Teal"
        self.user_id = None

        self.theme_cls.theme_style = ('Light')
        self.window = Builder.load_file("main.kv")

        return self.window


BusTracking().run()
