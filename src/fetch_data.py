from .classes.Event import Event
from datetime import datetime
import requests

# --- HERE WE FETCH DATA AND FORM MESSAGES TO BE SENT TO THE USER ---


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

    # Return the created event
    return event


# Function that retches data based on a keyword sent by the user and returns some matching events
def fetch_query(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/events/?tags_filter=' + keyword[0]
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    events = []
    try:
        for item in sample_arr:
            event = create_event(item)
            events.append(event)

        print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time,
              events[0].link)
    except:
        print('keyword not valid')
    return events


# Function that fetches a list of events near the location sent by user and returns three of them
def fetch_nearby(lat, lon):
    url = 'http://open-api.myhelsinki.fi/v1/events/?distance_filter=' + str(lat) + '%2C' + str(lon) + '%2C2'
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    events = []

    for item in sample_arr:
        event = create_event(item)
        events.append(event)

    print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time)

    return events


# Function that fetches data from Helsinki open API and returns data from it
def fetch_data():
    url = "http://open-api.myhelsinki.fi/v1/event/helsinki:af2e5ay52i"
    data = requests.get(url).json()
    info = data['name']['fi']
    print(info)
    return info


# Function that forms the data fetched by the previous functions and forms it into a message
# that can be sent to the user
def create_message_text(event):
    msg_text = '<b>' + event.name + '</b>' + '\nOsoite: ' + event.address + '\n\n' + event.desc + '\n\nAlkaa: ' + \
               datetime_to_str(event.start_time)

    # Only shows the Päättyy: ... -field if ending date exists
    if isinstance(event.end_time, datetime):
        msg_text = msg_text + '\nPäättyy: ' + datetime_to_str(event.end_time)

    # Only shows the Lue lisää... -field if link exists
    if event.link is not None:
        msg_text = msg_text + '\n\n<a href=\"' + event.link + '\">Lue lisää...</a>'

    return msg_text
