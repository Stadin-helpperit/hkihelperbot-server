from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import threading

import telegramcalendar
from fetch_data import fetch_all, fetch_nearby, fetch_query, fetch_by_date
from create_msg import create_message_text
import telegram

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
def search(update, context):
    searchresult = fetch_query(all_events, context.args[0])
    # Search results should be looped and send more results to user, but for now it only send first one's name
    if len(searchresult) > 0:
        for item in searchresult:
            if item.img_link is not None:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=item.img_link,
                                       caption=create_message_text(item), parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item)
                                         , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No events matching keyword. Use command like /search (keyword)')


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
def button_inline_handler(update, context):
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
