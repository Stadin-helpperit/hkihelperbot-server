from bot import helptext, nearby, handle_search_date, searchdate_inline_handler, \
    cal_inline_handler, \
    trains, route, handle_search_events, search_event_inline_handler, \
    handle_search_activities, search_activities_inline_handler, search_inline_handler, handle_search, \
    location_inline_handler, handle_search_places, search_places_inline_handler
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

# This handler listens for the command "/start" and calls the previously defined caps function
helptext_handler = CommandHandler("help", helptext)
dispatcher.add_handler(helptext_handler)


# This handler listens for user's messages and calls the previously defined search function
search_handler = CommandHandler('search', handle_search)
dispatcher.add_handler(search_handler)

# This handler listens for user's messages and calls the previously defined handle_search_events function
event_handler = CommandHandler('events', handle_search_events)
dispatcher.add_handler(event_handler)

# This handler listens for user's messages and calls the previously defined handle_search_activities function
activity_handler = CommandHandler('activities', handle_search_activities)
dispatcher.add_handler(activity_handler)

# This handler listens for user's messages and calls the previously defined search function
place_handler = CommandHandler('places', handle_search_places)
dispatcher.add_handler(place_handler)

# This handler listens for user's messages and calls the previously defined trains function
trains_handler = CommandHandler('trains', trains)
dispatcher.add_handler(trains_handler)

# This handler listens for user's messages and calls the previously defined trains function
route_handler = CommandHandler('from', route)
dispatcher.add_handler(route_handler)

# This handler listens for user's messages and calls the previously defined nearby function
nearby_handler = MessageHandler(Filters.location & (~Filters.command), nearby)
dispatcher.add_handler(nearby_handler)

# handler that listens for /searchdate
searchdate_handler = CommandHandler('searchdate', handle_search_date)
dispatcher.add_handler(searchdate_handler)

# handler for /search inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(search_inline_handler, pattern='k'))

# handler for /search inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(search_event_inline_handler, pattern='t'))

# handler for /search_activities inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(search_activities_inline_handler, pattern='a'))

# handler for /search_places inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(search_places_inline_handler, pattern='p'))

# handler for /searchdate inline keyboard buttons
updater.dispatcher.add_handler(CallbackQueryHandler(searchdate_inline_handler, pattern='i'))

# handler for searched events, activ, or places results locations lookup inline keyboard button "Show location"
updater.dispatcher.add_handler(CallbackQueryHandler(location_inline_handler, pattern='l'))

# handler for calendar inline buttons
updater.dispatcher.add_handler(CallbackQueryHandler(cal_inline_handler))
