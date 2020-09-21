import telegram, os, logging, requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime

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
    def __init__(self, name='', lat=0.0, lon=0.0, address='', desc='', start_time='', end_time='', link=None):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.desc = desc
        self.start_time = start_time
        self.end_time = end_time
        self.link = link


def str_to_datetime(date_string):
    date_time_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_time_object


def datetime_to_str(date_time_object):
    if isinstance(date_time_object, datetime):
        date_string = date_time_object.strftime("%d.%m.%Y, %H:%M")
    else:
        date_string = date_time_object
    return date_string


# Function creates an Event-class object from an database item
def create_event(item):
    # Create an empty event
    event = Event()

    # Set the English name for the event and if it doesn't exist choose the Finnish name
    if item['name']['en'] is not None:
        event.name = item['name']['en']
    elif item['name']['fi'] is not None:
        event.name = item['name']['fi']
    else:
        event.name = 'Ei ilmoitettua nimeä'

    # Set the address if it exists
    if item['location']['address']['street_address'] is not None:
        event.address = item['location']['address']['street_address']
    else:
        event.address = 'Ei ilmoitettua osoitetta'

    # Set the starting and ending dates of the event
    if item['event_dates']['starting_day'] is None:
        event.start_time = 'Ei ilmoitettua aloituspäivämäärää'
    else:
        event.start_time = str_to_datetime(item['event_dates']['starting_day'])

    if item['event_dates']['ending_day'] is None:
        event.end_time = 'Ei ilmoitettua lopetuspäivämäärää'
    else:
        event.end_time = str_to_datetime(item['event_dates']['ending_day'])

    # Set coordinates for the event
    event.lat = item['location']['lat']
    event.lon = item['location']['lon']

    # Set the description of the event
    if item['description']['intro'] is None:
        event.desc = 'Kuvausta ei saatavilla'
    else:
        event.desc = item['description']['intro']

    # Set the info link url of the event
    event.link = item['info_url']

    # Return the created event
    return event


# Function that retches data based on a keyword sent by the user and return some matching events
def fetch_query(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/events/?tags_filter=' + keyword[0]
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    events = []
    try:
        for item in sample_arr:
            event = create_event(item)
            events.append(event)

        print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time, events[0].link)
    except:
        print('keyword not valid')
    return events


# This function fetches a list of events near the users location and returns three of them
def fetch_nearby(lat, lon):
    url = 'http://open-api.myhelsinki.fi/v1/events/?distance_filter=' + str(lat) + '%2C' + str(lon) + '%2C2'
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    events = []

    for item in sample_arr:
        event = create_event(item)
        events.append(event)

    print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time)

    return events


# This function takes an event and creates a message to be sent to the user
def create_message_text(event):
    msg_text = '<b>' + event.name + '</b>' + '\nOsoite: ' + event.address + '\n\n' + event.desc + '\n\nAlkaa: ' + \
               datetime_to_str(event.start_time)

    # Only shows the Päättyy: ... -field if ending date exists
    if isinstance(event.end_time, datetime):
        msg_text = msg_text + '\nPäättyy: ' + datetime_to_str(event.end_time)

    # Only shows the Lue lisää... -field if link exists
    if event.link is not None:
        msg_text = msg_text + '\n\n<a href=\"' + event.link + '\">Lue lisää...</a>'

    return msg_text


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
    if len(searchresult) > 0:
        for item in searchresult:
            context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item)
                                     , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No events matching keyword')

# Function that echoes the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Function that sends the given text back in all caps as a message
def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# Gets the user's location if they send one and returns three events near the location
def nearby(update, context):
    user = update.message.from_user
    user_location = update.message.location
    print('Location of ' + user.first_name + ': lat:', user_location.latitude, ' lon:',
          user_location.longitude)
    event_data = fetch_nearby(user_location.latitude, user_location.longitude)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Lähimmät tapahtumasi (3 ensimmäistä osumaa): ')

    # send 3 events and addresses from nearby results list
    for item in event_data:

        #if item.name == event_data[1].name:
            # if current event has same start time and name then start time should have multiple dates.
         #   item.start_time = str('useita aikoja: \n' + str(item.start_time) + str(event_data[1].start_time))
          #  print(item.start_time)

        #if item.name == event_data[2].name:

         #   item.start_time = str('useita aikoja: \n' + str(item.start_time) + str(event_data[2].start_time))

      #  if item.name == event_data[1].name and item.name == event_data[2].name:
       #     break

        context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item), parse_mode=telegram.ParseMode.HTML,
                                             disable_web_page_preview=True)
        context.bot.send_location(chat_id=update.effective_chat.id, latitude=item.lat, longitude=item.lon)


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
