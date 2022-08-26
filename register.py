from email.mime.text import MIMEText
import smtplib
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from firebase_admin import auth
from database import create_db


class RegisterScreen(Screen):
    # storing check box value in this string
    user_category_value = StringProperty()

    def register_driver(self):
        key = ['Full_Name', 'Password', "contact_number", "E-Mail"]
        user_data = {}

        registration_name = self.ids.driver_register_full_name.text
        registration_number = self.ids.driver_register_number.text
        registration_password = self.ids.driver_register_password.text
        registration_email = self.ids.driver_email.text
        # print((self.user_category_value))

        val = [registration_name, registration_password,
               registration_number, registration_email]
        for i in range(len(key)):
            user_data[key[i]] = val[i]

            if (len(registration_name) == 0 and len(registration_number) == 0 and len(registration_password) == 0):
                toast("Enter all the Details")
                cancel_btn_username_dialogue = MDFlatButton(
                    text='Retry', on_release=self.close_dilougebox)
                self.dialog = MDDialog(title="Notification", text="Enter all the Details", size_hint=(
                    0.7, 0.2), buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
            else:

                create_db(self.user_category_value,
                          registration_number, user_data)
                try:

                    self.create_authentication_account(
                        registration_email, registration_number, registration_password)
                except Exception as e:
                    toast("Authentication Registration Error.")

        # except:
            # cancel_btn_username_dialogue = MDFlatButton(
            #     text='Retry', on_release=self.close_dilougebox)
            # self.dialog = MDDialog(title="Notification", text="Enter all the Details", size_hint=(
            #     0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            # self.dialog.open()
            # toast("Enter all the details")

    def close_dilougebox(self, obj):
        self.dialog.dismiss()

    def create_authentication_account(self, email, phone_number, password):

        auth.create_user(email=email,
                         phone_number=phone_number, password=password)

        try:

            self.send_email(email)
            toast("Registration Sucessfull.")
            self.manager.current = 'userlogin'
            self.manager.transition.direction = 'left'

        except:
            toast("Error on e-mail verification")

    def send_email(self, email):
        try:
            link = auth.generate_email_verification_link(
                email=email)
            message = MIMEText(f'{link}')
            message['Subject'] = 'Email Verification Link'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("fashiongaze10@gmail.com", "vvgrkowsykpdxhdh")
            server.sendmail("fashiongaze10@gmail.com",
                            email, message.as_string())
            server.quit()
            toast("Verification Link Sent")
        except Exception as e:
            toast("Problem on E-mail Verification")
