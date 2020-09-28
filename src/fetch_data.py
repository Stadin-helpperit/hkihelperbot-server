from src.create_event import create_event
import requests

# --- HERE WE FETCH DATA AND FORM MESSAGES TO BE SENT TO THE USER ---


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
