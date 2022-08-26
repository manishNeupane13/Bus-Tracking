
import pyrebase


firebaseConfig = {'apiKey': "AIzaSyBYndj6gNz2Y6CRHAs11GQRAxug35OWWk8",
                  'authDomain': "bus-tracking-9720b.firebaseapp.com",
                  'databaseURL': "https://bus-tracking-9720b-default-rtdb.asia-southeast1.firebasedatabase.app",
                  'projectId': "bus-tracking-9720b",
                  'storageBucket': "bus-tracking-9720b.appspot.com",
                  'messagingSenderId': "309426687559",
                  'appId': "1:309426687559:web:11a08c6e5d8aa28032ab62",
                  'measurementId': "G-FCQ26QWTSW"
                  }
firebase_conn = pyrebase.initialize_app(firebaseConfig)
real_time_db = firebase_conn.database()

# email = input("Enter your Email")
# password = input("Enter your password")


# firebase_conn.auth().sign_in_with_email_and_password(email,password)
# firebase_conn.auth().create_user_with_email_and_password(email, password)
# bus_details = real_time_db.child("Bus Details").get()
# mob_number=[]
# bus_number=[]

# for x in bus_details.each():
#     if "Kalanki-TIA" in x.val().values():
#         print(x.key())
#         print(x.val().keys())
# # print(key[0])

# print(type(x))
# print(x.val())
# for val in x.val():
#     print(val)


# def get_real_time_location():
#     location_list = []
#     # one_location_info = []
#     real_data = real_time_db.child("Real Tiime Location Data").child().get()
#     for x in real_data.each():

#         one_location_info=[]
#         #break the first loop when route name is found inside the database
#         first_loop=False
#         for val in x.val().values():
#             if "" ==val['Route_Name']:
#                 one_location_info.append(val['Latitude'])
#                 one_location_info.append(val['Longitude'])
#                 first_loop=True
#                 break
#         if first_loop==True:
#             location_list.append(one_location_info)
#             continue


#     return(location_list)


#     # return latitude,longitude  0

# print (get_real_time_location())



def create_db(user_category, mobile_number, user_data):
    return real_time_db.child("Registration Database").child(user_category).child(mobile_number).set(user_data)


def fetch_db(user_category, mobile_number):
    return real_time_db.child("Registration Database").child(user_category).child(mobile_number).get()

# def fetech_route():
#     return real_time_db.child("Kathmandu Bus Route List").get()


def fetch_user_login_info(user_category, mobile_number):
    user_number = real_time_db.child(
        "Registration Database").child(user_category).get()
    password = real_time_db.child("Registration Database").child(
        user_category).child(mobile_number).get()

    user_number.child(mobile_number).get()


def update_db(user_category, mobile_number, user_data):
    real_time_db.child("Registration Database").child(
        user_category).child(mobile_number).update(user_data)


def delete_db(user_category, mobile_number):
    return real_time_db.child("Registration Database").child(user_category).child(mobile_number).remove()
# create_db(user_category="asdf",mobile_number=9810438054,user_data={"name":"manish"})
# user_data=fetch_db("Service_User","9810438054")


# user_data=fetch_db('Service_User', '9814973122')
# user_data=fetech_route()
# for x in user_data.each():
#     print(x.val())
# (fetch_user_login_info("Service_User","9810438054"))
# user_key = 9814397082
# data = real_time_db.child("User Verification").child(
#     "Address Information").child(user_key).get()
# try:
#     for i in data.each():
#         print(i.key(),i.val())

# except:
#     print("No value found")
# try:
#     user_address_info=real_time_db.child("User Verification").child("General Information").child(user_key).get()
#     print(len(user_address_info.val()))
# except:


#     print("no value found")
# lat=27.7 
# lon=85.3

# real_data=firebase_conn.database().child("Real Tiime Location Data").get()
# for i in real_data.each():
#     for j in (i.val().values()):
#         if lat in j.values():
#             print(i.key(),j.values())
#             break
        
        
