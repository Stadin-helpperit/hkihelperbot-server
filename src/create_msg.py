from src.create_event import datetime_to_str
from datetime import datetime

# --- HERE WE FORM THE MESSAGES TO BE SENT TO THE USER ---


# This function takes an event and creates a message to be sent to the user
def create_message_text(event):
    msg_text = '<b>' + event.name + '</b>' + '\nOsoite: ' + event.address + '\n\n' + event.desc +  '\nTapahtuman tagit: ' + event.tags + '\n\nAlkaa: ' + \
               datetime_to_str(event.start_time)

    # Only shows the Päättyy: ... -field if ending date exists
    if isinstance(event.end_time, datetime):
        msg_text = msg_text + '\nPäättyy: ' + datetime_to_str(event.end_time)

    # Only shows the Lue lisää... -field if link exists
    if event.link is not None:
        msg_text = msg_text + '\n\n<a href=\"' + event.link + '\">Lue lisää...</a>'

    return msg_text
