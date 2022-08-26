from geopy.geocoders import Nominatim
from geopy import distance
loc = Nominatim(user_agent='GetLoc')


def get_location_name(lat, lon):
    # print(lat, lon)

    location_name = loc.reverse((lat, lon))
    return location_name.address


def get_distance_travelled(location_one, location_two):
    getLoc1 = loc.geocode(f'{location_one},kathmandu')
    getloc2 = loc.geocode(f'{location_two},kathmandu')
    location1 = (getLoc1.latitude, getLoc1.longitude)
    location2 = (getloc2.latitude, getloc2.longitude)
    return (distance.distance(location1[:2], location2[:2]))


def get_lat_and_lon(location_name):
    getLoc1 = loc.geocode(location_name)
    return (getLoc1.latitude, getLoc1.longitude)


# # name = (get_location_name(27.83, 85.34))
# # print(name.split(",")[0])
# print(get_distance_travelled(
#     location_one="Kantipur Academy of Health Sciences", location_two="Jai Nepal Hall"))
