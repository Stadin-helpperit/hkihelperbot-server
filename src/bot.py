import telegram, os, logging, urllib.request, requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Loads the api token from the .env file
load_dotenv()

# Logger, print's out info in case something is going wrong
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Creating an Updater object, continuously fetches new updates from Telegram
updater = Updater(token=os.environ.get("API_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


# Function that retches data based on a keyword sent by the user and return some matching events
def fetch_query(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/events/?tags_filter=' + keyword[0]
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:15]
    names = []
    for item in sample_arr:
        if item['name']['en'] is None:
            if item['name']['fi'] is None:
                # if name is null, go to next iteration
                continue
            else:
                names.append(item['name']['fi'])
        else:
            names.append(item['name']['en'])
    names = ", ".join(names)
    print(names)
    return names


# This function fetches a list of events near the users location and returns three of them
def fetch_nearby(lat, lon):
    url = 'http://open-api.myhelsinki.fi/v1/events/?distance_filter=' + str(lat) + '%2C' + str(lon) + '%2C2'
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    names = []
    for item in sample_arr:
        if item['name']['en'] is None:
            if item['name']['fi'] is None:
                # if name is null, go to next iteration
                continue
            else:
                names.append(item['name']['fi'])
        else:
            names.append(item['name']['en'])
    names = ", ".join(names)
    print(names)
    return names


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
    context.bot.send_message(chat_id=update.effective_chat.id, text=searchresult)


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
    nearbyresult = fetch_nearby(user_location.latitude, user_location.longitude)
    context.bot.send_message(chat_id=update.effective_chat.id, text=nearbyresult)


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
