from datetime import datetime
import pytz, json
from telegram import InlineKeyboardButton
from emoji import emojize


# Helper functions to reformat date/time data

# This function constructs the help message for the user
with open("../tag_keyboard.json") as json_data:
    tag_keyboard_data = json.load(json_data)


def str_to_datetime(date_string):
    date_time_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    from_zone_utc = pytz.utc
    to_zone_local = pytz.timezone("Europe/Helsinki")
    date_time_object = date_time_object.replace(tzinfo=from_zone_utc)
    date_time_object = date_time_object.astimezone(to_zone_local)
    return date_time_object


def datetime_to_str(date_time_object):
    if isinstance(date_time_object, datetime):
        date_string = date_time_object.strftime("%d.%m.%Y, %H:%M")
    else:
        date_string = date_time_object
    return date_string


# Function that creates buttons for tag keyboard by chosen data type, tag list and columns amount
def create_buttons(tag_list, columns, data_type):
    print(tag_list["tags"])
    tag_keyboard = []
    tag_keyboard_row = []
    for tag in tag_list["tags"]:
        new_button = InlineKeyboardButton(text=(emojize(tag["tag"] + ' ' + tag["emoji"], use_aliases=True)), callback_data=data_type + '_' + tag["key"])
        tag_keyboard_row.append(new_button)
        if len(tag_keyboard_row) == columns:
            tag_keyboard.append(tag_keyboard_row)
            tag_keyboard_row = []
    return tag_keyboard


# Function that creates tag keyboard markup by calling create_buttons
def create_tag_keyboard_markup(data_type):
    # p = places, t = events, a = activities
    if data_type == 'p':
        keyboard_markup = create_buttons(tag_keyboard_data[1], 2, data_type)
    else:
        keyboard_markup = create_buttons(tag_keyboard_data[0], 3, data_type)
    return keyboard_markup
