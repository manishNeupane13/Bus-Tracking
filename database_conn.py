
# import smtplib
# from firebase_admin import auth
# from email.mime.text import MIMEText


import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def realtime_db_connection():

    firebaseConfig = {'apiKey': "AIzaSyBKD_g1I3qXi4ZvaUMiZaJsqRcWsC3FDYA",
                      'authDomain': "bus-tracking-9720b.firebaseapp.com",
                      'databaseURL': "https://bus-tracking-9720b-default-rtdb.asia-southeast1.firebasedatabase.app",
                      'projectId': "bus-tracking-9720b",
                      'storageBucket': "bus-tracking-9720b.appspot.com",
                      'messagingSenderId': "309426687559",
                      'appId': "1:309426687559:web:11a08c6e5d8aa28032ab62",
                      'measurementId': "G-FCQ26QWTSW"
                      }
    firebase_conn = pyrebase.initialize_app(firebaseConfig)

    # auth = firebase_conn.auth()
    # email = "neupanemanes@gmail.com"
    # password = "123456"
    # # user = auth.create_user_with_email_and_password(email, password)
    # login = auth.sign_in_with_email_and_password(email, password)
    # auth.send_email_verification(login['idToken'])
    # auth.send_password_reset_email(email)

    return firebase_conn
# database()

# print(realtime_db_connection().database())
# print(realtime_db_connection().storage())


def firestore_db_connection():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

    # user = auth.create_user(email="neupanemanes@gmail.com",
    #                         phone_number="+9779810438054", password="123456")
    # link = (auth.generate_sign_in_with_email_link(
    #     email="neupanemanes@gmail.com", action_code_settings=None))
    # link = auth.generate_email_verification_link(
    #     email="neupanemanes@gmail.com")

    # link=(auth.generate_password_reset_link(email="neupanemanes@gmail.com",action_code_settings=None))
    # message = MIMEText(f'{link}')
    # message['Subject'] = 'Email Verification Link'

    # # message = "fsaldkjfsldfadslkf"
    # # print(link)

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.login("fashiongaze10@gmail.com", "vvgrkowsykpdxhdh")
    # server.sendmail("fashiongaze10@gmail.com",
    #                 "neupanemanes@gmail.com", message.as_string())
    # server.quit()

    # print(auth.get_user_by_phone_number("+9779810438054").email_verified)


#
# (firestore_db_connection())
# realtime_db_connection()

# realtime_db_connection().storage().child("eh").put("images//logo//new_logo.png")
# database_ref=realtime_db_connection()
# database_ref.database().child("Payment Details").child("Service User").child(9810438054).set(
#     {"Payment ID": 1, "Paid To":"", "Initial Location":"", "Final Destination ": "", 'Distance Travelled': "", 'Amount Paid ':""})
# database_ref.database().child("Payment Details").child(
#     "Service Provider").child(self.driver_number).set({"Payment ID": id, "Paid By": self.user_key, "Payer Category": self.user_cateogry, "Initial Location": self.inital_location, "Final Destination ": self.final_stand_name, 'Distance Travelled': self.distance_travelled, 'Amount Paid ': self.fareamount})
