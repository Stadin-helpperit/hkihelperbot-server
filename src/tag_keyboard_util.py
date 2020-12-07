from telegram import InlineKeyboardButton
from emoji import emojize
from pathlib import Path
import json

# Helper functions to create inline keyboards for selecting search keywords

# Resolves the current path
path = Path(__file__).parent / "../tag_keyboard.json"

# Opens the jsondata
with open(path) as json_data:
    tag_keyboard_data = json.load(json_data)


# Function that creates buttons for tag keyboard by chosen data type, tag list and columns amount
def create_buttons(tag_list, columns, data_type):
    print(tag_list["tags"])
    tag_keyboard = []
    tag_keyboard_row = []
    for tag in tag_list["tags"]:
        new_button = InlineKeyboardButton(text=(emojize(tag["tag"] + ' ' + tag["emoji"], use_aliases=True)),
                                          callback_data=data_type + '_' + tag["key"])
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
