import time 
import googlemaps 
import telepot
from telepot.loop import MessageLoop
from pprint import pprint
from GoogleAPI import get_nearest_location
import pdb 
from telepot.delegate import pave_event_space, per_chat_id, create_open
import json 
import os.path
import sys
from datetime import datetime
from configparser import ConfigParser

with open ('key.json') as f:
    input_keys = json.loads(f.read())
    TOKEN = input_keys['auth']['Token']
    API_KEY = input_keys['auth']['API_Key']
places_types = ['posto de gasolina', 'posto de saude']



FILE_NAME = "StoredRatings.txt"
chat_id = 0
gmaps = googlemaps.Client(key=API_KEY)
def read_ratings(file_name):
    if not os.path.isfile(FILE_NAME):
        stored_ratings = {}
        return stored_ratings
    with open (FILE_NAME) as f:
        stored_ratings = json.loads(f.read())
        return stored_ratings

def write_ratings(stored_ratings): 
    file = open(FILE_NAME, "w")
    encoded_dict = json.dumps(stored_ratings)
    file.write(encoded_dict)
    file.close()

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.state = 'prompt for type'

    def prompt_for_type(self, msg):
        self.sender.sendMessage('Digite: posto de gasolina ou posto de saude')
        self.state = 'type received'
        return self.state

    # Prompts user for the origin's address
    def prompt_for_address(self, msg):
        if msg['text'].lower() in places_types:
            self.location_type = msg['text'].lower()
            self.state = 300
        return self.state

    def prompt_for_radius(self, msg):
        self.users_address_longitude = msg['location']['longitude']
        self.users_address_latitude = msg['location']['latitude']
        self.users_address = gmaps.reverse_geocode((self.users_address_latitude, self.users_address_longitude))
        self.users_address = self.users_address[0]['formatted_address']
        self.sender.sendMessage('Por favor, coloque a distancia em metros para verificarmos os postos mais próximos')
        self.state = 'radius received'
        return self.state

    # Prompts user for their rating of the location
    def prompt_for_rating(self, msg):
        stripped_radius = msg['text'].strip()
        if str.isnumeric(stripped_radius) == True:
            self.radius_in_metres = int(msg['text'])
            chat_id = str(telepot.glance(msg)[2])
            nearest_location = get_nearest_location(self.users_address, self.radius_in_metres, chat_id, stored_ratings, self.location_type)
            self.sender.sendMessage(nearest_location['location_for_user'])
            self.sender.sendMessage('Classifique: Banheiro limpo - (1) sim ou (2) não')
            self.state = 'rating received'
        else:
            self.state = 'radius received'
            self.sender.sendMessage('Distancia em metros incorreta, insira novamente')
            return self.state

    # Formats the user's rating to a dictionary to be stored on the drive later
    def store_rating(self, stored_ratings, location_id, user_rating):
        if chat_id not in stored_ratings:
            stored_ratings[chat_id] = {}
        user_stored_ratings = stored_ratings[chat_id]
        if location_id not in user_stored_ratings:
            user_stored_ratings[location_id] = []
        user_stored_ratings[location_id].append(user_rating)
        write_ratings(stored_ratings)

    # Stores the user's rating  on the drive
    def store_check_ratings(self, msg):
        stripped_rating = msg['text'].strip()
        if str.isnumeric(stripped_rating) == True and int(msg['text']) <= 5 and int(msg['text']) >1:
            user_rating = int(msg['text'])
            chat_id = str(telepot.glance(msg)[2])
            location_id = get_nearest_location(self.users_address, self.radius_in_metres, chat_id, stored_ratings,self.location_type)['location_id']
            self.store_rating( stored_ratings, location_id, user_rating)
            self.sender.sendMessage('Por favor, compartilhe um novo endereço se você quiser usar o bot novamente')
            self.state = 'address received'
        else: 
            self.state = 'rating received'
            self.sender.sendMessage('Endereco invalido')
        return self.state
    
    # Terminates the bot
    def terminate_bot(self, msg):
        self.sender.sendMessage('Obrigado por usar o bot. Para reutilizar o bot, digite / start. Tenha um bom dia!')
        return 

    # Handles the states
    def on_chat_message(self, msg):
        if 'text' in msg and msg['text'] == '/stop':
            self.terminate_bot(msg)
        elif msg == '/start' or self.state == 'prompt for type':
            self.prompt_for_type(msg)
        elif self.state == 'type received':
            self.prompt_for_address(msg)
        elif self.state == 'address received':
            self.prompt_for_radius(msg)
        elif self.state == 300:
            self.prompt_for_rating(msg)
        elif self.state == 'rating received':
            self.store_check_ratings(msg)

    
stored_ratings = read_ratings(FILE_NAME)

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=3000),
])
MessageLoop(bot).run_as_thread()

while 1: 
    time.sleep(3000)
