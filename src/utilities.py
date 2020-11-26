from datetime import datetime
import pytz
from telegram import InlineKeyboardButton


# Helper functions to reformat date/time data


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


def create_tag_keyboard_markup(data_type):
    # List of popular tags that is used when the /search-command is invoked without a parameter
    if data_type == 'p':
        popular_tags = [['accomodation', '\U0001F3E8 Majoitus'],
                        ['sights & attractions', '\U0001F5FC Nähtävyydet'],
                        ['nature & sports', '\U0001F332\U000026BD Luonto ja liikunta'],
                        ['museums & galleries', '\U0001F3A8 Museot ja galleriat'],
                        ['restaurants & cafes', '\U0001F372 Ravintolat ja kahvilat'],
                        ['sauna & wellness', '\U0001F9D6 Hyvinvointi'],
                        ['venues', '\U0001F3DB Tapahtumapaikat'],
                        ['services', '\U0001F689 Palvelut'],
                        ['bars & nightlife', '\U0001F37B Baarit ja yöelämä'],
                        ['work & study', '\U0001F4DA Työt ja opiskelu']]
    else:
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
    if data_type == 'p':
        for tag in popular_tags:
            new_button = InlineKeyboardButton(text=tag[1], callback_data=data_type + '_' + tag[0])
            tag_keyboard_row.append(new_button)
            if len(tag_keyboard_row) == 2:
                tag_keyboard.append(tag_keyboard_row)
                tag_keyboard_row = []
    else:
        for tag in popular_tags:
            new_button = InlineKeyboardButton(text=tag[1], callback_data=data_type + '_' + tag[0])
            tag_keyboard_row.append(new_button)
            if len(tag_keyboard_row) == 3:
                tag_keyboard.append(tag_keyboard_row)
                tag_keyboard_row = []

    return tag_keyboard
