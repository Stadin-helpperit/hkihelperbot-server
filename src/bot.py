import threading
from datetime import datetime, timedelta

import telegram
from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import telegramcalendar
from create_msg import create_help_msg
from create_msg import create_message_text, create_message_train, create_message_text_activity, \
    create_message_text_place
from create_weather import create_weather_msg
from create_weather import fetch_weather
from fetch_data import fetch_all_events, fetch_nearby, fetch_query, fetch_by_date, fetch_trains, \
    fetch_activities_by_keyword, fetch_all_activities, fetch_all_places, fetch_places_by_keyword
from fetch_hsl_data import fetch_hsl_route, create_route_msg, fetch_search_address
from tag_keyboard_util import create_tag_keyboard_markup

# a processed list of all events to be fetched once an hour and should be used by all functions
all_events = []
all_activities = []
all_places = []

# --- SCHEDULED FUNCTIONS TO FETCH AND PROCESS DATA FROM MYHELSINKI API

# 3600 seconds = 1 hour
WAIT_SECONDS = 3600


# fetch and process all events every hour
def sched_fetch():
    print('Scheduled fetch beginning')
    global all_events
    global all_activities
    global all_places
    all_events = fetch_all_events()
    all_activities = fetch_all_activities()
    all_places = fetch_all_places()
    print('Scheduled fetch done')

    """for item in all_places:
        print(item.name + ' : ')
        print(item.tags)"""

    threading.Timer(WAIT_SECONDS, sched_fetch).start()


# initial fetch when starting the bot
sched_fetch()


# --- HERE WE DEFINE DIFFERENT FUNCTIONS THAT SEND MESSAGES ---

def handle_search(update, context):
    keyboard = [[InlineKeyboardButton(text='Events', callback_data='k1'),
                 InlineKeyboardButton(text='Activities', callback_data='k2'),
                 InlineKeyboardButton(text='Places', callback_data='k3')]]

    # if the user gives a parameter, the function will search content based on the user given search word
    # otherwise the function will send the keyboard for further questions
    if context.args:
        # check if the user has provided a search word, otherwise calls the appropriate handle_search_[event_type]
        if len(context.args) > 1:
            if context.args[0] == 'event':
                search_events(update, context, (' '.join(context.args[1:])))
            elif context.args[0] == 'activity':
                search_activities(update, context, (' '.join(context.args[1:])))
            elif context.args[0] == 'place':
                search_places(update, context, (' '.join(context.args[1:])))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Error. The correct syntax for the '
                                                                                'command is /search [event, activity'
                                                                                ' or place] [search word]. The'
                                                                                ' parameters in the brackets are'
                                                                                ' optional.')
        else:
            if context.args[0] == 'event':
                handle_search_events(update, context, True)
            elif context.args[0] == 'activity':
                handle_search_activities(update, context, True)
            elif context.args[0] == 'place':
                handle_search_places(update, context, True)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Error. The correct syntax for the '
                                                                                'command is /search [event, activity'
                                                                                ' or place] [search word]. The'
                                                                                ' parameters in the brackets are'
                                                                                ' optional.')
    else:
        reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Do you want to search for events, activities or places?', reply_markup=reply_markup)


def search_inline_handler(update, context):
    query = update.callback_query
    if query.data == 'k1':
        handle_search_events(update, context)
        query.edit_message_text(text="Searching for events... ")
    elif query.data == 'k2':
        handle_search_activities(update, context)
        query.edit_message_text(text="Searching for activites... ")
    elif query.data == 'k3':
        handle_search_places(update, context)
        query.edit_message_text(text="Searching for places...")


# Handles the button to check location for result after each Event, Activity, or Place
def location_inline_handler(update):
    query = update.callback_query
    if query.data == 'l1':
        # TODO: handle get events/activitys.. location and send it to user via bot.send_location
        query.edit_message_text(text="Looking up the search result's locations... ")
    pass


# a function to search events by keyword
def search_events(update, context, search_word):
    search_result = fetch_query(all_events, search_word)
    # Search results should be looped and send more results to user, but for now it only send first one's name
    if len(search_result) > 0:
        for item in search_result:
            if item.img_link is not None:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=item.img_link,
                                       caption=create_message_text(item), parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item),
                                         parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No events matching the keyword. Try to use the command like this: /search ("
                                      "keyword)")


def handle_search_activities(update, context, set_context_args_to_null=False):
    # set context.args to an empty list when this function is called with the /search-function
    if set_context_args_to_null:
        context.args = []

    print(update)
    # create tag keyboard markup with parameter datatype as 'a' for activities
    tag_keyboard = create_tag_keyboard_markup('a')

    # if the user gives a parameter the search_activities() function is called
    if context.args:
        msg = update.message.reply_text('Searching for activities with the tag {}...'.format(' '.join(context.args)))
        search_activities(update, context, ' '.join(context.args))
        msg.edit_text('Activities with the tag {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Search for activites with a tag. Some popular tags:',
                                 reply_markup=reply_markup)
        # update.message.reply_text('Hae aktiviteetteja tagilla. Suosittuja tageja:', reply_markup=reply_markup)


# a function to search activities by keyword
def search_activities(update, context, search_word):
    search_result = fetch_activities_by_keyword(all_activities, search_word)
    # Search results should be looped and send more results to user, but for now it only send first one's name
    if len(search_result) > 0:
        for item in search_result:
            msg_text = create_message_text_activity(item)
            # Media limit with image = 1024 characters, remove the image from results if msg_text > 1024
            if item.img_link is not None and len(msg_text) < 1024:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=item.img_link,
                                       caption=msg_text, parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text,
                                         parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No activities matching the keyword. Try to use the command like this: /search ("
                                      "keyword)")


# TODO: ask for further information about places (about subcategories)
# a function to search places by keyword
def search_places(update, context, search_word):
    search_result = fetch_places_by_keyword(all_places, search_word)
    # Search results should be looped and send more results to user, but for now it only send first one's name
    if len(search_result) > 0:
        for item in search_result:
            msg_text = create_message_text_place(item)
            # Media limit with image = 1024 characters, remove the image from results if msg_text > 1024
            if item.img_link is not None and len(msg_text) < 1024:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=item.img_link,
                                       caption=msg_text, parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text,
                                         parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No places matching the keyword. Try to use the command like this: /search ("
                                      "keyword)")


# Function that fetches trains from VR/rata.digitraffic API with requested parameters and returns timetable in message
def trains(update, context):
    if context.args:
        trains_result = fetch_trains(context.args)
        for item in trains_result:
            context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_train(item),
                                     parse_mode=telegram.ParseMode.HTML)
    else:
        msgtext = \
            'Write the station code after /trains to get ' \
            'the arriving and departing trains for that ' \
            'station.\n\nFor example, the station code for ' \
            'Helsinki Central Train station is HKI.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msgtext)


def route(update, context):
    hsl_fetch_result = None
    from_address_and_loc = None
    to_address_and_loc = None

    if context.args:
        to_index = context.args.index('to')
        from_name = '%20'.join(context.args[0:to_index])
        to_name = '%20'.join(context.args[to_index + 1:])
        try:
            from_address_and_loc = fetch_search_address(from_name)
            to_address_and_loc = fetch_search_address(to_name)

            print(from_address_and_loc + ':::' + to_address_and_loc)

            try:
                hsl_fetch_result = fetch_hsl_route(from_address_and_loc, to_address_and_loc)

                if hsl_fetch_result['data']['plan']['itineraries']:
                    routemsg = create_route_msg(hsl_fetch_result)
                else:
                    routemsg = "Route not found :( Try adding the city's name after the address(es), it might help!"

                context.bot.send_message(chat_id=update.effective_chat.id, text=routemsg,
                                         parse_mode=telegram.ParseMode.HTML)
            except (TypeError, IndexError) as error:
                errormsg = "Something unexpected went wrong :crying_face: :white_flag: " \
                           "My data source might be having problems finding a route. I'm so sorry!"

                context.bot.send_message(chat_id=update.effective_chat.id, text=emojize(errormsg))
                print("Error handled in function route():", error)

        except (IndexError, IndexError) as error:
            errormsg = "For some reason I couldn't find the address. You can check that you spelled the address " \
                       "correctly or maybe my source for address data is having problems :face_with_rolling_eyes:"
            context.bot.send_message(chat_id=update.effective_chat.id, text=emojize(errormsg))
            print("Error handled in function route():", error)

    else:
        routemsg = "Write the starting and destination addresses after the command. Like this:\n\n" \
                   "/from ratapihantie 13 to Pietari Kalmin Katu 15"

        context.bot.send_message(chat_id=update.effective_chat.id, text=routemsg,
                                 parse_mode=telegram.ParseMode.HTML)


def weather(update, context):
    weatherdata = fetch_weather()
    weathermsg = create_weather_msg(weatherdata)
    context.bot.send_message(chat_id=update.effective_chat.id, text=weathermsg, parse_mode=telegram.ParseMode.HTML)


# Function that sends the given text back in all caps as a message
def helptext(update, context):
    text_help = create_help_msg()

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)


# Gets the user's location if they send one and returns three events near the location
def nearby(update, context):
    user = update.message.from_user
    user_location = update.message.location
    print('Location of ' + user.first_name + ': lat:', user_location.latitude, ' lon:',
          user_location.longitude)
    event_data = fetch_nearby(user_location.latitude, user_location.longitude)
    if len(event_data) > 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here\'s the events near you: ')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No events found nearby')

    # send 3 events and maps from nearby results list
    for item in event_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item),
                                 parse_mode=telegram.ParseMode.HTML,
                                 disable_web_page_preview=True)
        context.bot.send_location(chat_id=update.effective_chat.id, latitude=item.lat, longitude=item.lon)


# This function handles the user pressing a button on a calendar keyboard
def cal_inline_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(context.bot, update)
    if selected:
        query = update.callback_query
        query.edit_message_text(text='Looking for events on {}...'.format(date.strftime('%d.%m.%Y')))
        search_date(update, context, date.strftime('%d.%m.%Y'))
        query.edit_message_text(text='Events on {}:'.format(date.strftime('%d.%m.%Y')))


# This function handles the user pressing a button on an inline keyboard
def searchdate_inline_handler(update, context):
    def date_to_str(daysdelta=0):
        date = datetime.now() + timedelta(days=daysdelta)
        return date.strftime('%d.%m.%Y')

    query = update.callback_query
    if query.data == 'i1':
        query.edit_message_text(text="Looking up events happening today... ")
        search_date(update, context, date_to_str())
        query.edit_message_text(text="Events happening today: ")
    elif query.data == 'i2':
        query.edit_message_text(text="Looking up events happening tomorrow... ")
        search_date(update, context, date_to_str(1))
        query.edit_message_text(text="Events happening tomorrow: ")
    elif query.data == 'i3':
        query.edit_message_text(text="Choose the date: ", reply_markup=telegramcalendar.create_calendar())


# This function will handle the user command /searchdate
# If a parameter is given by the user, this will call the search_date function
# otherwise it will invoke the inline keyboard to ask the date
def handle_search_date(update, context):
    if context.args:
        msg = update.message.reply_text('Looking for events on {}...'.format(context.args[0]))
        search_date(update, context, context.args[0])
        msg.edit_text('Events on {}:'.format(context.args[0]))
    else:
        keyboard = [[InlineKeyboardButton(text='Today', callback_data='i1'),
                     InlineKeyboardButton("Tomorrow", callback_data='i2')],
                    [InlineKeyboardButton("Choose the date", callback_data='i3')]]
        reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Choose a date to look up events on:', reply_markup=reply_markup)


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_event_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Looking for events with the tag '{}'...".format(search_word))
    search_events(update, context, search_word)
    query.edit_message_text(text="Event's matching the tag '{}': ".format(search_word))


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_activities_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Looking up activities with the tag '{}'...".format(search_word))
    search_activities(update, context, search_word)
    query.edit_message_text(text="Activities matching the tag '{}': ".format(search_word))


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_places_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Looking up places with the tag '{}'...".format(search_word))
    print("DEBUG: SELECTED PLACES")
    search_places(update, context, search_word)
    query.edit_message_text(text="Places matching the tag '{}': ".format(search_word))


# This function handles the /search -command and either passes the parameter given by user to the search() function
# or sends the inline tag keyboard to the user which is handled by search_inline_keyboard()
def handle_search_events(update, context, set_context_args_to_null=False):
    # set context.args to an empty list when this function is called with the /search-function
    if set_context_args_to_null:
        context.args = []
    # create tag keyboard markup with parameter datatype as 't' for events
    tag_keyboard = create_tag_keyboard_markup('t')

    # if the user gives a parameter the search() function is called
    if context.args:
        msg = update.message.reply_text('Looking up events with the tag {}...'.format(' '.join(context.args)))
        search_events(update, context, ' '.join(context.args))
        msg.edit_text('Events matching the tag {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Search for events with a tag. Some popular '
                                                                        'tags:',
                                 reply_markup=reply_markup)


# This function handles the /search -command and either passes the parameter given by user to the search() function
# or sends the inline tag keyboard to the user which is handled by search_inline_keyboard()
def handle_search_places(update, context, set_context_args_to_null=False):
    # set context.args to an empty list when this function is called with the /search-function
    if set_context_args_to_null:
        context.args = []
    # create tag keyboard markup with parameter datatype as 'p' for places
    tag_keyboard = create_tag_keyboard_markup('p')

    # if the user gives a parameter the search_places() function is called
    if context.args:
        msg = update.message.reply_text('Looking up places with the tag {}...'.format(' '.join(context.args)))
        search_places(update, context, ' '.join(context.args))
        msg.edit_text('Places matching the tag {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Search for places with a tag. Some popular '
                                                                        'tags:',
                                 reply_markup=reply_markup)


# This function will call fetch_by_date and send the user three events on a given date
def search_date(update, context, date):
    date = date.split(".")
    date = date[2] + '-' + date[1] + '-' + date[0] + 'T12:00:00.000Z'
    print(date)
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    searchresult = fetch_by_date(all_events, date)

    if len(searchresult) > 0:
        for item in searchresult:
            if item.img_link is not None:
                print(item.img_link)
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=item.img_link,
                                       caption=create_message_text(item), parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item),
                                         parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No events on the chosen date')
