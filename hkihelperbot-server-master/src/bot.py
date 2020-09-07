import telegram
import os
import logging
import urllib.request
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Loads the api token from the .env file
load_dotenv()

# Logger, print's out info in case something is going wrong
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Creating an Updater object, continously fetches new updates from Telegram
updater = Updater(token=os.environ.get("API_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

# Function that retches data based on a keyword sent by the user and return some matching events


def fetch_query(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/events/?tags_filter=' + keyword[0]
    data = requests.get(url).json()
    results = data['data']
    sampleArr = results[:15]
    names = ''
    for item in sampleArr:
        if item['name']['en'] == None:
            continue
        else:
            names += item['name']['en'] + ', '
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
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# test fetch function to send data from json api


def info(update, context):
    infomsg = fetch_data()
    context.bot.send_message(chat_id=update.effective_chat.id, text=infomsg)

# test fetch function to send data from json api


def search(update, context):
    searchresult = fetch_query(context.args)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=searchresult)

# Function that echoes the user's messages


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)

# Function that sends the given text back in all caps as a message


def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


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

# This handler listens for user's messages and calls the previously defined echo function
search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

# handler that listens for /info
info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

# starts the polling of messages
updater.start_polling()
