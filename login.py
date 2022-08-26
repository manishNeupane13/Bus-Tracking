
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from firebase_admin import auth
from kivy.app import App

import smtplib
from firebase_admin import auth
from email.mime.text import MIMEText


class LoginScreen(Screen):
    app = App.get_running_app()
    database_ref = app.realtime_database
    user_category_value = StringProperty()
    firebase_auth = database_ref.auth()

    def close_dilougebox(self, obj):
        self.dialog.dismiss()

    def check_login(self):
        userName = self.ids.driver_login_username.text
        userEmail = self.ids.driver_email.text
        UserPassword = self.ids.driver_login_password.text
        # print(userEmail, userName, UserPassword)

        # print((self.user_category_value, userName, UserPassword))
        # login_result = fetch_db(self.user_category_value, userName)
        try:
            self.auth_login(userEmail, userName, UserPassword)
        except Exception as e:
            # print(e)
            toast("Authenticaiton Unsucessfull")
        # try:
        #     # for x in login_result.each():
        #         # print(self.user_category_value)
        #         # print(self.user_category_value == 'Service_user')
        #         # print(x.key(), x.val())
        #         if (self.user_category_value == 'Service_User' and x.key() == 'Password' and x.val() == UserPassword):

        #         else:
        #             toast("Please Enter Correct Credentials.")

        # elif(self.user_category_value == 'Service_Provider' and x.key() == 'Password' and x.val() == UserPassword):
        #     self.manager.current = 'homenav'
        #     self.manager.transition.direction = "left"

        # except:
        #     cancel_btn_username_dialogue = MDFlatButton(
        #         text='Retry', on_release=self.close_dilougebox)
        #     self.dialog = MDDialog(title=" Invalid Ceridentails ", text="Please input enter a valid Ceridentials", size_hint=(
        #         0.7, 0.2), buttons=[cancel_btn_username_dialogue])
        #     self.dialog.open()
        #     toast("Enter all the Details.")

    def auth_login(self, email, phone_number, password):
        try:

            self.firebase_auth.sign_in_with_email_and_password(
                email, password)
            try:

                if (auth.get_user_by_phone_number(phone_number).email_verified == True):
                    toast("Login Sucessfull.")
                    self.manager.current = 'userhome'
                    self.manager.transition.direction = "left"
            except Exception as e:
                toast("Contact Number Verification Unsucessful.")
        except Exception as e:
            # print(e)
            toast("Credentials Not Matched.")

    def reset_password(self,):

        email = self.ids.driver_email.text
        if (len(email) != 0):
            try:

                link = (auth.generate_password_reset_link(
                    email=email, action_code_settings=None))
                message = MIMEText(f'{link}')
                message['Subject'] = 'Password Reset Link'

                # message = "fsaldkjfsldfadslkf"
                # print(link)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login("fashiongaze10@gmail.com", "vvgrkowsykpdxhdh")
                server.sendmail("fashiongaze10@gmail.com",
                                email, message.as_string())
                server.quit()
                toast("Password Reset Link Sent.")
            except Exception as e:
                print(e)
                toast("Password Reset Link Not Send.")
        else:
            toast("Please Enter the email")
