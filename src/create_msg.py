from datetime_util import datetime_to_str
from datetime import datetime
from emoji import emojize
import re
import json

# --- HERE WE FORM THE MESSAGES TO BE SENT TO THE USER ---

# This function constructs the help message for the user
with open("../commands_help.json") as json_data:
    help_cmd_info = json.load(json_data)


def create_help_msg():

    help_msg = "Alright, lets get you started! :relieved_face: \n\n" \
                "Here's all of the ways I can help you: \n\n"

    for cmd in help_cmd_info:
        help_msg += cmd['emoji'] + " " + cmd['syntax'] + " | " + cmd['explanation'] + "\n\n"

    return emojize(help_msg)


# This function takes an event and creates a message to be sent to the user
def create_message_text(event):
    msg_text = '<b>' + event.name + '</b>' + '\nAddress: ' + event.address + '\n\n' + event.desc \
               + "\n\nEvent's tags: " + ', '.join(event.tags) + '\n\nStarting time: ' + \
               datetime_to_str(event.get_sorted_start_times()[0])  # TODO: korjaa pvm

    # Only shows the Päättyy: ... -field if ending date exists
    if isinstance(event.end_time, datetime):
        msg_text = msg_text + '\nEndtime: ' + datetime_to_str(event.end_time)

    # TODO: korjaa niin että näkyy oikea pvm
    if len(event.start_time) > 1:
        msg_text = msg_text + '\nAlso on: '
        counter = 0
        for time in event.get_sorted_start_times()[1:-1]:
            # maximum five dates to avoid clutter
            if counter > 4:
                break
            msg_text = msg_text + datetime_to_str(time) + '\n'
            counter += 1

    # Only shows the Lue lisää... -field if link exists
    if event.link is not None:
        msg_text = msg_text + '\n\n<a href=\"' + event.link + '\">Read more...</a>'

    return msg_text


def create_message_train(train):
    msg_text = '<b>' + 'From: ' + train.departure + ', track ' + train.fromTrack + ' to ' + train.arrival + ', track ' + train.toTrack + '</b>' \
               + '\nTrain number: ' + train.train_type + str(train.number) \
               + '\nTime: ' + str(train.datetime) + ', train type: ' + train.train_category + ', line: ' + train.line_id
    return msg_text


def create_message_text_activity(activity):
    msg_text = '<b>' + activity.name + '</b>' + '\nAddress: ' + activity.address + '\n\n' + cleanhtml(activity.desc) \
               + "\n\nActivitie's tags: " + ', '.join(activity.tags) + '\n\nWhen and where: ' + activity.where_and_when \
               + '\n\nKesto: ' + activity.duration

    return msg_text


def create_message_text_place(place):
    msg_text = '<b>' + place.name + '</b>' + '\nAddress: ' + place.address + '\n\n' + cleanhtml(place.desc) \
               + "\n\nPlace's tags: " + ', '.join(
        place.tags)

    return msg_text


# Poistaa ylimääräiset html-tagit body-tekstistä
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
