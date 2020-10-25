from test.google_response_mock import return_fake_vals
import requests
from geopy.geocoders import Nominatim
from geopy import geocoders
import sys
import configparser

maps_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
google_api_key = ''

def get_city_lat_long(city_name):
  geolocator = Nominatim(user_agent="food-desert")
  location = geolocator.geocode(city_name)
  print(location.raw)
  return location.latitude, location.longitude

def call_google_locations_api(latitude, longitude, radius, keyword_type, keyword=None):
  params = {
    'location': str(latitude) + ',' + str(longitude),
    'radius': str(radius),
    'type': keyword_type,
    'key': google_api_key
  }
  if keyword:
    params['keyword'] = keyword
  r = requests.get(url = maps_url, params=params) 
  data = r.json() 
  return data

def get_num_restaurants(latitude, longitude, radius):
  res = call_google_locations_api(latitude, longitude, radius, 'restaurant', 'fast')
  return len(res['results'])

def get_num_grocery_stores(latitude, longitude, radius):
  res = call_google_locations_api(latitude, longitude, radius, 'supermarket')
  return len(res['results'])

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print('Wrong argument passed. Need to pass in config.txt path')
    sys.exit()

  config = configparser.ConfigParser()
  config.read(sys.argv[1])
  google_api_key = config.get("settings","google_api_key")
 
  radius_meters = 1000
  latitude, longitute = get_city_lat_long('Sagamihara')
  
  # restaurants = get_num_restaurants(latitude, longitute, radius_meters)
  # grocery = get_num_grocery_stores(latitude, longitute, radius_meters)
  # score = restaurants / grocery
  # print(score)
  