from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from fetch_data import fetch_all, fetch_nearby, fetch_query, fetch_by_date, fetch_trains, fetch_stations, fetch_activities_by_keyword
from fetch_hsl_data import fetch_hsl_route, create_route_msg
from create_msg import create_message_text, create_message_train, create_message_text_activity
import telegram
import threading
import telegramcalendar

# a processed list of all events to be fetched once an hour and should be used by all functions
all_events = []


# --- SCHEDULED FUNCTIONS TO FETCH AND PROCESS DATA FROM MYHELSINKI API

# 3600 seconds = 1 hour
WAIT_SECONDS = 3600


# fetch and process all events every hour
def sched_fetch():
    print('Scheduled fetch beginning')
    global all_events
    all_events = fetch_all()
    print('Scheduled fetch done')

    """for item in all_events:
        print(item.name + ' : ')
        for time in item.start_time:
            print(time)"""

    threading.Timer(WAIT_SECONDS, sched_fetch).start()


# initial fetch when starting the bot
sched_fetch()


# --- HERE WE DEFINE DIFFERENT FUNCTIONS THAT SEND MESSAGES ---


# Function that sends a message ""I'm a bot, please talk to me!""
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# a function to search events by keyword
def search(update, context, search_word):
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


# a function to search activities by keyword
def search_activities(update, context):
    search_result = fetch_activities_by_keyword(context.args[0])
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


# Function that echoes the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Function that fetches trains from VR/rata.digitraffic API with requested parameters and returns timetable in message
def trains(update, context):
    trainsresult = fetch_trains(context.args)
    for item in trainsresult:
        context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_train(item),
                                 parse_mode=telegram.ParseMode.HTML)


def button_selection_handler(update, context):
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


def stations_selection(update, context, scope):
    stationslist = fetch_stations()
    msg_text = ''
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    if scope == 'a-f':
        for item in stationslist[:20]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
            else:
                continue
    elif scope == 'g-n':
        for item in stationslist[21:40]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
            else:
                continue
    elif scope == 'o-ö':
        for item in stationslist[41:60]:
            if item['type'] == 'STATION':
                msg_text = (msg_text + ', ' + item['stationName'] + ' - ' + item['stationShortCode'] + '\n')
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
def search_inline_handler(update, context):
    query = update.callback_query

    search_word = query.data.split('_')[1]

    query.edit_message_text(text="Etsitään tapahtumia tagilla '{}'...".format(search_word))
    search(update, context, search_word)
    query.edit_message_text(text="Tapahtumat tagilla '{}': ".format(search_word))


# This function handles the /serach -command and either passes the parameter given by user to the search() function
# or sends the inline tag keyboard to the user which is handled by search_inline_keyboard()
def handle_search(update, context):
    # List of popular tags that is used when the /search-command is invoked without a parameter
    popular_tags = [['music', '\U0001F3B6 Musiikki'],
                    ['theatre', '\U0001F3AD Teatteri'],
                    ['culture', '\U0001F3A8 Kulttuuri'],
                    ['sports', '\U000026BD Urheilu'],
                    ['museums', '\U0001F3DB Museot'],
                    ['nature', '\U0001F332 Luonto'],
                    ['food', '\U0001F372 Ruoka'],
                    ['families with children', '\U0001F46A Perheille'],
                    ['workshops', '\U0001F6E0 Työpajat']]

    # some functionality to turn the list of tags into telegram keyboard markup
    tag_keyboard = []
    tag_keyboard_row = []
    for tag in popular_tags:
        new_button = InlineKeyboardButton(text=tag[1], callback_data='t_' + tag[0])
        tag_keyboard_row.append(new_button)
        if len(tag_keyboard_row) == 3:
            tag_keyboard.append(tag_keyboard_row)
            tag_keyboard_row = []

    # if the user gives a parameter the search() function is called
    if context.args:
        msg = update.message.reply_text('Etsitään tapahtumia tagilla {}...'.format(' '.join(context.args)))
        search(update, context, ' '.join(context.args))
        msg.edit_text('Tapahtumat tagilla {}:'.format(' '.join(context.args)))
    # else will send the tag keyboard
    else:
        reply_markup = InlineKeyboardMarkup(tag_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text('Hae tapahtumaa tagilla. Suosittuja tageja:', reply_markup=reply_markup)


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
