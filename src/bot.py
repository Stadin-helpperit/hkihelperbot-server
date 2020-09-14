import telegram, os, logging, urllib.request, requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Loads the api token from the .env file
load_dotenv()
token = os.environ.get("API_TOKEN")
# Logger, print's out info in case something is going wrong
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Creating an Updater object, continuously fetches new updates from Telegram
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Universal class for blank event to be used to create instances of events
class Event:
    def __init__(self, name, lat=0.0, lon=0.0, address='', desc='', start_time='', end_time=''):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.desc = desc
        self.start_time = start_time
        self.end_time = end_time

# Function that retches data based on a keyword sent by the user and return some matching events
def fetch_query(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/events/?tags_filter=' + keyword[0]
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:15]
    events = []
    for item in sample_arr:
        if item['name']['en'] is None:
            if item['name']['fi'] is None:
                # if name is null, go to next iteration
                continue
            else:
                event = Event(item['name']['fi'])
        else:
            event = Event(item['name']['en'])
        event.address = item['location']['address']['street_address']
        if item['event_dates']['starting_day'] is None:
            event.start_time = ' Ei ilmoitettua aloituspäivämäärää'
        else:
            event.start_time = item['event_dates']['starting_day'][0:9]

        if item['event_dates']['ending_day'] is None:
            event.end_time = ' Ei ilmoitettua lopetuspäivämäärää'
        else:
        # event_dates can be None in some cases!
            event.end_time = item['event_dates']['ending_day'][0:9]

        if item['description']['intro'] is None:
            event.desc = 'Kuvausta ei saatavilla '
        else:
            event.desc = item['description']['intro']

        events.append(event)

    print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time)

    # print(events)
    return events


# This function fetches a list of events near the users location and returns three of them
def fetch_nearby(lat, lon):
    url = 'http://open-api.myhelsinki.fi/v1/events/?distance_filter=' + str(lat) + '%2C' + str(lon) + '%2C2'
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    events = []
    event_location = data['data'][0]['location']
    for item in sample_arr:
        if item['name']['en'] is None:
            if item['name']['fi'] is None:
                # if name is null, go to next iteration
                continue
            else:
                event = Event(item['name']['fi'])
        else:
            event = Event(item['name']['en'])
        event.lat = item['location']['lat']
        event.lon = item['location']['lon']
        event.address = item['location']['address']['street_address']
        event.desc = item['description']['intro']
        # event_dates can be None in some cases!
        event.start_time = item['event_dates']['starting_day'][0:9]
        event.end_time = item['event_dates']['ending_day'][0:9]
        events.append(event)

    print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time)
    for lat, lon in event_location.items():
        event_lat = lat
        event_lon = lon
        print(lat, lon)

    return events


# Function that fetches data from Helsinki open API and returns data from it
def fetch_data():
    url = "http://open-api.myhelsinki.fi/v1/event/helsinki:af2e5ay52i"
    data = requests.get(url).json()
    info = data['name']['fi']
    print(info)
    return info

# --- HERE WE DEFINE DIFFERENT FUNCTIONS THAT SEND MESSAGES ---


# Function that sends a message ""I'm a bot, please talk to me!""
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# test fetch function to send data from json api
def info(update, context):
    infomsg = fetch_data()
    context.bot.send_message(chat_id=update.effective_chat.id, text=infomsg)


# test fetch function to send data from json api
def search(update, context):
    searchresult = fetch_query(context.args)
    # Search results should be looped and send more results to user, but for now it only send first one's name
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + searchresult[0].name + "</b>" + '\nOsoite: ' + searchresult[0].address + '\n\n' + searchresult[0].desc
                             + '\n\nAlkaa: ' + searchresult[0].start_time + '\nPäättyy: ' + searchresult[0].end_time, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + searchresult[1].name + "</b>" + '\nOsoite: ' + searchresult[1].address + '\n\n' + searchresult[1].desc
                             + '\n\nAlkaa: ' + searchresult[1].start_time + '\nPäättyy: ' + searchresult[1].end_time, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + searchresult[2].name + "</b>" + '\nOsoite: ' + searchresult[2].address + '\n\n' + searchresult[2].desc
                             + '\n\nAlkaa: ' + searchresult[2].start_time+ '\nPäättyy: ' + searchresult[2].end_time, parse_mode=telegram.ParseMode.HTML)



# Function that echoes the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Function that sends the given text back in all caps as a message
def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# This function should be made to send location on a map
def location(update, context):
    #location = fetch_nearby()
    #requests.post(f'https://api.telegram.org/{token}/sendlocation?chat_id={update.effective_chat.id}&latitude={}&longitude={}')
    pass

# Gets the user's location if they send one and returns three events near the location
def nearby(update, context):
    user = update.message.from_user
    user_location = update.message.location
    print('Location of ' + user.first_name + ': lat:', user_location.latitude, ' lon:',
          user_location.longitude)
    event_data = fetch_nearby(user_location.latitude, user_location.longitude)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Lähimmät tapahtumasi (3 ensimmäistä osumaa): ')
    # send 3 events and addresses from nearby results list
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + event_data[0].name + "</b>" + '\nOsoite: ' + event_data[0].address + '\n\n' + event_data[0].desc
                             + "\n\nAlkaa: " + event_data[0].start_time + '\nPäättyy: ' + event_data[0].end_time, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_location(chat_id=update.effective_chat.id, latitude=event_data[0].lat, longitude=event_data[0].lon)

    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + event_data[1].name + "</b>" + '\nOsoite: ' + event_data[1].address + '\n\n' + event_data[1].desc
                             + "\n\nAlkaa: " + event_data[1].start_time + '\nPäättyy: ' + event_data[1].end_time, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_location(chat_id=update.effective_chat.id, latitude=event_data[1].lat, longitude=event_data[1].lon)

    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>" + event_data[2].name + "</b>" + '\nOsoite: ' + event_data[2].address + '\n\n' + event_data[2].desc
                             + "\n\nAlkaa: " + event_data[2].start_time + '\nPäättyy: ' + event_data[2].end_time, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_location(chat_id=update.effective_chat.id, latitude=event_data[2].lat, longitude=event_data[2].lon)


# --- HERE WE CREATE HANDLER TYPE OBJECTS THAT LISTEN FOR COMMAND AND CALL THE DESIRED FUNCTIONS ---

# This handler listens for the command "/start" and calls the previously defined
# start function
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# This handler listens for the command "/start" and calls the previously defined caps function
caps_handler = CommandHandler("caps", caps)
dispatcher.add_handler(caps_handler)

# This handler listens for user's messages and calls the previously defined echo function
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# This handler listens for user's messages and calls the previously defined search function
search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

# This handler listens for user's messages and calls the previously defined nearby function
nearby_handler = MessageHandler(Filters.location & (~Filters.command), nearby)
dispatcher.add_handler(nearby_handler)

# handler that listens for /info
info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

# starts the polling of messages
updater.start_polling()
