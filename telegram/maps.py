import googlemaps
from pprint import pprint
from datetime import datetime
from googleplaces import GooglePlaces, types, lang
import json

with open ('key.json') as f:
    input_keys = json.loads(f.read())
    TOKEN = input_keys['auth']['Token']
    API_KEY = input_keys['auth']['API_Key']
gmaps = googlemaps.Client(key=API_KEY)
google_places = GooglePlaces(API_KEY)


def average(l):
    return sum(l) / len(l)

def deduplicate(l):
    return list(set(l))

def find_matching_indices(a, b):
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                yield j

def find_origin_coordinates(users_address):
    geocode_result = gmaps.geocode(users_address)
    lat_origin = geocode_result[0]['geometry']['location']['lat']
    lng_origin = geocode_result[0]['geometry']['location']['lng']
    origin_coordinates = (lat_origin, lng_origin)
    return origin_coordinates

def format_query_results(query_result):
    google_locations_ids = []
    for i in range (len(query_result.places)):
        query_result.places[i].get_details()
        location_id = query_result.places[i].name + query_result.places[i].formatted_address
        google_locations_ids.append(location_id)
    return google_locations_ids

def find_averages_of_ratings(indicies, google_locations_ids, stored_ratings, chat_id):
    averages_of_ratings = []
    for i in range(len(indicies)):
        location = google_locations_ids[indicies[i]]
        ratings = stored_ratings[chat_id][location]
        average_of_rating = average(ratings)
        averages_of_ratings.append(average_of_rating)
    return averages_of_ratings

def get_nearest_location(users_address, radius_in_metres, chat_id, stored_ratings, location_type):
    query_result = google_places.nearby_search(location=users_address, radius=int(radius_in_metres), types=[location_type])
    origin_coordinates = find_origin_coordinates(users_address)
    distances = [] 
    destinations = [] 
    google_locations_ids = []
    averages_of_ratings = []

    stored_locations_ids = list(stored_ratings[chat_id])
   
    google_locations_ids = format_query_results(query_result)
    google_locations_ids = deduplicate(google_locations_ids)

    list(find_matching_indices(stored_locations_ids, google_locations_ids))
    indicies = list(find_matching_indices(stored_locations_ids, google_locations_ids))
    
    averages_of_ratings = find_averages_of_ratings(indicies, google_locations_ids, stored_ratings, chat_id)

    for i in range(len(query_result.places)):
        lat_destination = query_result.places[i].geo_location['lat']
        lng_destination = query_result.places[i].geo_location['lng']
        destination_coordinates =  (lat_destination,lng_destination) 
        destinations.append(destination_coordinates)
        distance_details = gmaps.distance_matrix(origin_coordinates,destination_coordinates)
        distance = distance_details['rows'][0]['elements'][0]['distance']['value']
        distances.append(distance)
    for i in range(len(indicies)):
        distances[indicies[i]] = distances[indicies[i]] * (5 / averages_of_ratings[i])
    min_distance = distances.index(min(distances))
    query_result.places[min_distance].get_details()
    places_dict = {
        "location_for_user" : " ".join(list(("Seu destino deve ser ",\
        query_result.places[min_distance].name, " at " , query_result.places[min_distance].formatted_address ,\
        " O número de telefone deles é " , query_result.places[min_distance].local_phone_number , " e sua classificação é ",\
        str(query_result.places[min_distance].rating)))),
        "location_id" : query_result.places[min_distance].name + query_result.places[min_distance].formatted_address
    }
    return places_dict 
