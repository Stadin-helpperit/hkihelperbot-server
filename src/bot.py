from fetch_data import fetch_data, fetch_nearby, fetch_query
from create_msg import create_message_text
import telegram

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

    # send 3 events and addresses from nearby results list
    for item in event_data:
        # if item.name == event_data[1].name:
        # if current event has same start time and name then start time should have multiple dates.
        #   item.start_time = str('useita aikoja: \n' + str(item.start_time) + str(event_data[1].start_time))
        #  print(item.start_time)

        # if item.name == event_data[2].name:

        #   item.start_time = str('useita aikoja: \n' + str(item.start_time) + str(event_data[2].start_time))

        #  if item.name == event_data[1].name and item.name == event_data[2].name:
        #     break

        context.bot.send_message(chat_id=update.effective_chat.id, text=create_message_text(item),
                                 parse_mode=telegram.ParseMode.HTML,
                                 disable_web_page_preview=True)
        context.bot.send_location(chat_id=update.effective_chat.id, latitude=item.lat, longitude=item.lon)
