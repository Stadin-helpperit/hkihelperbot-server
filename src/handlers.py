from bot import start, caps, echo, search, nearby, info, handle_search_date, button_inline_handler, cal_inline_handler, \
    trains, route, stations, button_selection_handler
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from dotenv import load_dotenv
import os

# --- HERE WE CREATE HANDLER TYPE OBJECTS THAT LISTEN FOR COMMANDS AND CALL THE DESIRED FUNCTIONS ---

# Loads the api token from the .env file
load_dotenv()
token = os.environ.get("API_TOKEN")

# Creating an Updater object that continuously fetches new updates from Telegram
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

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

# This handler listens for user's messages and calls the previously defined trains function
trains_handler = CommandHandler('trains', trains)
dispatcher.add_handler(trains_handler)

# This handler listens for user's messages and calls the previously defined trains function
stationslist_handler = CommandHandler('stations', stations)
dispatcher.add_handler(stationslist_handler)

# This handler listens for user's messages and calls the previously defined trains function
route_handler = CommandHandler('route', route)
dispatcher.add_handler(route_handler)

# This handler listens for user's messages and calls the previously defined nearby function
nearby_handler = MessageHandler(Filters.location & (~Filters.command), nearby)
dispatcher.add_handler(nearby_handler)

# handler that listens for /info
info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

# handler that listens for /searchdate
searchdate_handler = CommandHandler('searchdate', handle_search_date)
dispatcher.add_handler(searchdate_handler)

# handler for event routing button
updater.dispatcher.add_handler(CallbackQueryHandler(button_selection_handler, pattern='s'))

# handler for inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(button_inline_handler, pattern='i'))

# handler for calendar inline buttons
updater.dispatcher.add_handler(CallbackQueryHandler(cal_inline_handler))


