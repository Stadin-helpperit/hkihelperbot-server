from datetime import datetime
from src.classes.Event import Event

# --- HERE WE FORM EVENT OBJECTS FROM FETCHED DATA ---


# Helper functions to reformat date/time data
def str_to_datetime(date_string):
    date_time_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_time_object


def datetime_to_str(date_time_object):
    if isinstance(date_time_object, datetime):
        date_string = date_time_object.strftime("%d.%m.%Y, %H:%M")
    else:
        date_string = date_time_object
    return date_string


# Helper function to create an Event-class object from a database item
def create_event(item):
    # Create an empty event
    event = Event()

    # Set the English name for the event and if it doesn't exist choose the Finnish name
    if item['name']['en'] is not None:
        event.name = item['name']['en']
    elif item['name']['fi'] is not None:
        event.name = item['name']['fi']
    else:
        event.name = 'Ei ilmoitettua nimeä'

    # Set the address if it exists
    if item['location']['address']['street_address'] is not None:
        event.address = item['location']['address']['street_address']
    else:
        event.address = 'Ei ilmoitettua osoitetta'

    # Set the starting and ending dates of the event
    if item['event_dates']['starting_day'] is None:
        event.start_time = 'Ei ilmoitettua aloituspäivämäärää'
    else:
        event.start_time = str_to_datetime(item['event_dates']['starting_day'])

    if item['event_dates']['ending_day'] is None:
        event.end_time = 'Ei ilmoitettua lopetuspäivämäärää'
    else:
        event.end_time = str_to_datetime(item['event_dates']['ending_day'])

    # Set coordinates for the event
    event.lat = item['location']['lat']
    event.lon = item['location']['lon']

    # Set the description of the event
    if item['description']['intro'] is None:
        event.desc = 'Kuvausta ei saatavilla'
    else:
        event.desc = item['description']['intro']

    # Set the info link url of the event
    event.link = item['info_url']

    # Set the tags for the event from list
    if len(item['tags']) < 1:
        event.tags = 'Tapahtumalla ei tageja'
    else:
        tags = item['tags']
        for i in tags:
            event.tags = event.tags + i['name'] + ', '

    # Return the created event
    return event

