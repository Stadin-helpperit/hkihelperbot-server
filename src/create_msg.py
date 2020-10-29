from create_event import datetime_to_str
from datetime import datetime

# --- HERE WE FORM THE MESSAGES TO BE SENT TO THE USER ---


# This function takes an event and creates a message to be sent to the user
def create_message_text(event):
    msg_text = '<b>' + event.name + '</b>' + '\nOsoite: ' + event.address + '\n\n' + event.desc \
               + '\n\nTapahtuman tagit: ' + ', '.join(event.tags) + '\n\nAlkaa: ' + \
               datetime_to_str(event.get_sorted_start_times()[0])  # TODO: korjaa pvm

    # Only shows the Päättyy: ... -field if ending date exists
    if isinstance(event.end_time, datetime):
        msg_text = msg_text + '\nPäättyy: ' + datetime_to_str(event.end_time)

    # TODO: korjaa niin että näkyy oikea pvm
    if len(event.start_time) > 1:
        msg_text = msg_text + '\nMyös: '
        counter = 0
        for time in event.get_sorted_start_times()[1:-1]:
            # maximum five dates to avoid clutter
            if counter > 4:
                break
            msg_text = msg_text + datetime_to_str(time) + '\n'
            counter += 1

    # Only shows the Lue lisää... -field if link exists
    if event.link is not None:
        msg_text = msg_text + '\n\n<a href=\"' + event.link + '\">Lue lisää...</a>'

    return msg_text


def create_message_train(train):
    msg_text = '<b>' + 'From: ' + train.departure + ', track ' + train.fromTrack + ' to ' + train.arrival + ', track ' + train.toTrack + '</b>' \
        + '\nJunanumero: ' + train.train_type + str(train.number) \
        + '\nAika: ' + str(train.datetime) + ', junan tyyppi: ' + train.train_category + ', linja: ' + train.line_id
    return msg_text
