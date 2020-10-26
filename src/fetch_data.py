from create_event import create_event
from create_train import create_train
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
    except Exception as ex:
        print(ex)
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

# Function that fetches trains from VR/rata.digitraffic API with requested parameters and returns timetable in message
def fetch_trains(station):
    result = requests.get("https://rata.digitraffic.fi/api/v1/live-trains/station/" + station[0] + "?minutes_before_departure=15&minutes_after_departure=15&minutes_before_arrival=15&minutes_after_arrival=15").json()
    # Array to save all train objects
    trains = []
    # Go through whole response json and create a Train instance and append it to array
    for item in result:
        train = create_train(item)
        trains.append(train)
    # Print example
    print(str(trains[0].number) + ', ' + trains[0].departure + ', ' + trains[0].arrival)
    return trains


# This function fetches all events from myHelsinki-api and filters items on a given day
def fetch_by_date(date):
    def get_start_time(item):
        if item['event_dates']['starting_day'] is None:
            return '999999999999999999'
        else:
            return item['event_dates']['starting_day']

    def filter_events(item):
        if get_start_time(item)[0:10] == date[0:10]:
            return True
        else:
            return False

    url = "http://open-api.myhelsinki.fi/v1/events/"
    data = requests.get(url).json()
    results = data['data']
    sample_array = filter(filter_events, results)
    results.sort(key=get_start_time)

    events = []
    for item in sample_array:
        print(item)
        event = create_event(item)
        events.append(event)
        if len(events) >= 3:
            break
    return events
