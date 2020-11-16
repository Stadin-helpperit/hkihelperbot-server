from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from fetch_data import fetch_all_events, fetch_nearby, fetch_query, fetch_by_date, fetch_trains, fetch_stations, \
    fetch_activities_by_keyword, fetch_all_activities, fetch_all_places, fetch_places_by_keyword
from fetch_hsl_data import fetch_hsl_route, create_route_msg
from create_msg import create_message_text, create_message_train, create_message_text_activity, create_message_text_place
from utilities import create_tag_keyboard_markup
import telegram
import threading
import telegramcalendar

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

    """for item in all_events:
        print(item.name + ' : ')
        for time in item.start_time:
            print(time)"""

    threading.Timer(WAIT_SECONDS, sched_fetch).start()


# initial fetch when starting the bot
sched_fetch()


# --- HERE WE DEFINE DIFFERENT FUNCTIONS THAT SEND MESSAGES ---

def handle_search(update, context):
    keyboard = [[InlineKeyboardButton(text='Events', callback_data='k1'),
                 InlineKeyboardButton(text='Activities', callback_data='k2'),
                 InlineKeyboardButton(text='Places', callback_data='k3')]]

    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Do you want to search for events, activities or places?', reply_markup=reply_markup)


def search_inline_handler(update, context):
    query = update.callback_query
    if query.data == 'k1':
        handle_search_events(update, context)
        query.edit_message_text(text="Etsitään tapahtumia... ")
    elif query.data == 'k2':
        handle_search_activities(update, context)
        query.edit_message_text(text="Etsitään aktiviteetteja... ")
    elif query.data == 'k3':
        handle_search_places(update, context)
        query.edit_message_text(text="Etsitään paikkoja...")


# Handles the button to check location for result after each Event, Activity, or Place
def location_inline_handler(update, context):
    query = update.callback_query
    if query.data == 'l1':
        # to do: handle get events/activitys.. location and send it to user via bot.send_location
        query.edit_message_text(text="Etsitään sijainnit hakutuloksille... ")
    pass


# Function that sends a message ""I'm a bot, please talk to me!""
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


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
                context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item)
                                         , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No events matching keyword. Use command like /search (keyword)')


def handle_search_activities(update, context):
    print(update)
    # create tag keyboard markup with parameter datatype as 'a' for activities
    tag_keyboard = create_tag_keyboard_markup('a')

    # if the user gives a parameter the search_activities() function is called
    if context.args:
        msg = update.message.reply_text('Etsitään aktiviteetteja tagilla {}...'.format(' '.join(context.args)))
        search_activities(update, context, ' '.join(context.args))
        msg.edit_text('Tapahtumat tagilla {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Hae aktiviteetteja tagilla. Suosittuja tageja:', reply_markup=reply_markup)
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
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text
                                         , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No events matching keyword. Use command like /search (keyword)')


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
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text
                                         , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No places matching keyword.')


# Function that echoes the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Function that fetches trains from VR/rata.digitraffic API with requested parameters and returns timetable in message
def trains(update, context):
    trains_result = fetch_trains(context.args)
    for item in trains_result:
        context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_train(item),
                                 parse_mode=telegram.ParseMode.HTML)


# Function that handles selection callback query for inline keyboard stations scope selection
def stations_button_selection_handler(update, context):
    query = update.callback_query
    if query.data == 's1':
        query.edit_message_text(text="Etsitään asemia A-F... ")
        scope = 'a-f'
        stations_selection(update, context, scope)
        query.edit_message_text(text="ASEMAT: ")
    elif query.data == 's2':
        query.edit_message_text(text="Etsitään asemia G-N... ")
        scope = 'g-n'
        stations_selection(update, context, scope)
        query.edit_message_text(text="ASEMAT: ")
    elif query.data == 's3':
        query.edit_message_text(text="Etsitään asemia O-Ö... ")
        scope = 'o-ö'
        stations_selection(update, context, scope)
        query.edit_message_text(text="ASEMAT: ")


# Function that lists all station shortcodes with matching stations for user to use with /trains command
def stations(update, context):
    keyboard = [[InlineKeyboardButton(text='A-F', callback_data='s1'),
                 InlineKeyboardButton("G-N", callback_data='s2')],
                [InlineKeyboardButton("O-Ö", callback_data='s3')]]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Valitse asemalyhenteet väliltä:', reply_markup=reply_markup)


# Function that sends selected scope of stations and asks use if he wants location of the station on map
def stations_selection(update, context, scope):
    stations_list = fetch_stations()
    msg_text = ''
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    if scope == 'a-f':
        for item in stations_list[:20]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
            else:
                continue
    elif scope == 'g-n':
        for item in stations_list[21:40]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
            else:
                continue
    elif scope == 'o-ö':
        for item in stations_list[41:60]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
            else:
                continue

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)
    handle_lookup_station_loc(update, context)


# Function that prints inline button for user to look up locations
def handle_lookup_station_loc(update, context):
    # inline-button for location lookup.
    loc_search_btn = [[InlineKeyboardButton(text='Sijainti', callback_data='w1')]]

    reply_markup = InlineKeyboardMarkup(loc_search_btn, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Etsi aseman sijainti?', reply_markup=reply_markup)


# Function that handles callback query for inline button asking if user wants selected stations locations
def station_info_inline_handler(update, context):
    query = update.callback_query
    if query.data == 'w1':
        query.edit_message_text(text="Etsitään asemien sijainnit... ")
        station_locations_search(update, context)


# TEST CODE for this functionality: Function that sends some locations to user if user chooses so from the inline button
def station_locations_search(update, context):
    stations_list = fetch_stations()
    print(update)
    msg_text = ''

    for item in stations_list[:5]:
        if item['type'] == 'STATION':
            msg_text = (msg_text + 'Station: ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n' +
                        'Station location: ' + str(item['longitude']) + ' and ' + str(item['latitude']) + '\n')
            context.bot.send_location(chat_id=update.effective_chat.id, latitude=item['latitude'], longitude=item['longitude'])
        else:
            continue
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


def route(update, context):
    routemsg = create_route_msg()
    for item in range(len(routemsg)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=routemsg[item])


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
        query.edit_message_text(text='Etsitään tapahtumia päivämäärällä {}...'.format(date.strftime('%d.%m.%Y')))
        search_date(update, context, date.strftime('%d.%m.%Y'))
        query.edit_message_text(text='Tapahtumat päivämäärällä {}:'.format(date.strftime('%d.%m.%Y')))


# This function handles the user pressing a button on an inline keyboard
def searchdate_inline_handler(update, context):
    def date_to_str(daysdelta=0):
        date = datetime.now() + timedelta(days=daysdelta)
        return date.strftime('%d.%m.%Y')

    query = update.callback_query
    if query.data == 'i1':
        query.edit_message_text(text="Etsitään tapahtumia tänään... ")
        search_date(update, context, date_to_str())
        query.edit_message_text(text="Tapahtumat tänään: ")
    elif query.data == 'i2':
        query.edit_message_text(text="Etsitään tapahtumia huomenna... ")
        search_date(update, context, date_to_str(1))
        query.edit_message_text(text="Tapahtumat huomenna: ")
    elif query.data == 'i3':
        query.edit_message_text(text="Valitse päivämäärä: ", reply_markup=telegramcalendar.create_calendar())


# This function will handle the user command /searchdate
# If a parameter is given by the user, this will call the search_date function
# otherwise it will invoke the inline keyboard to ask the date
def handle_search_date(update, context):
    if context.args:
        msg = update.message.reply_text('Etsitään tapahtumia päivämäärällä {}...'.format(context.args[0]))
        search_date(update, context, context.args[0])
        msg.edit_text('Tapahtumat päivämäärällä {}:'.format(context.args[0]))
    else:
        keyboard = [[InlineKeyboardButton(text='Tänään', callback_data='i1'),
                     InlineKeyboardButton("Huomenna", callback_data='i2')],
                    [InlineKeyboardButton("Valitse päivämäärä", callback_data='i3')]]
        reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Miltä ajalta haluat tapahtumia:', reply_markup=reply_markup)


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_event_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Etsitään tapahtumia tagilla '{}'...".format(search_word))
    search_events(update, context, search_word)
    query.edit_message_text(text="Tapahtumat tagilla '{}': ".format(search_word))


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_activities_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Etsitään aktiviteetteja tagilla '{}'...".format(search_word))
    search_activities(update, context, search_word)
    query.edit_message_text(text="Aktiviteetit tagilla '{}': ".format(search_word))


# This function handles the user pressing a button on an inline keyboard with tag selection
def search_places_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Etsitään paikkoja tagilla '{}'...".format(search_word))
    print("DEBUG: SELECTED PLACES")
    search_places(update, context, search_word)
    query.edit_message_text(text="Paikat tagilla '{}': ".format(search_word))


# This function handles the /search -command and either passes the parameter given by user to the search() function
# or sends the inline tag keyboard to the user which is handled by search_inline_keyboard()
def handle_search_events(update, context):
    # create tag keyboard markup with parameter datatype as 't' for events
    tag_keyboard = create_tag_keyboard_markup('t')

    # if the user gives a parameter the search() function is called
    if context.args:
        msg = update.message.reply_text('Etsitään tapahtumia tagilla {}...'.format(' '.join(context.args)))
        search_events(update, context, ' '.join(context.args))
        msg.edit_text('Tapahtumat tagilla {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hae tapahtumaa tagilla. Suosittuja tageja:', reply_markup=reply_markup)


# This function handles the /search -command and either passes the parameter given by user to the search() function
# or sends the inline tag keyboard to the user which is handled by search_inline_keyboard()
def handle_search_places(update, context):
    # create tag keyboard markup with parameter datatype as 'p' for places
    tag_keyboard = create_tag_keyboard_markup('p')

    # if the user gives a parameter the search() function is called
    if context.args:
        msg = update.message.reply_text('Etsitään paikkoja tagilla {}...'.format(' '.join(context.args)))
        search_places(update, context, ' '.join(context.args))
        msg.edit_text('Paikat tagilla {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hae paikkoja tagilla. Suosittuja tageja:',
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
                context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item)
                                         , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No events on chosen date')
