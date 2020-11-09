from create_event import create_event, str_to_datetime
from create_train import create_train
from create_activity import create_activity
from create_place import create_place
import requests

# --- HERE WE FETCH DATA AND FORM MESSAGES TO BE SENT TO THE USER ---


# Function that fetches data based on a keyword sent by the user and returns some matching events
def fetch_query(all_events, keyword):
    def filter_events_by_tag(item):
        if keyword in item.tags:
            return True
        else:
            return False

    results = list(filter(filter_events_by_tag, all_events))
    query_result_events = results[:3]
    """events = []
    try:
        for item in sample_arr:
            event = create_event(item)
            events.append(event)

        print(events[0].name, events[0].lat, events[0].lon, events[0].address, events[0].start_time, events[0].end_time,
              events[0].link)
    except Exception as ex:
        print(ex)
        print('keyword not valid')"""
    return query_result_events



    


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


    # Function that fetches a list of activities near the location sent by user and returns three of them
def fetch_activities_by_keyword(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/activities/?tags_search=' + keyword 
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    print(sample_arr)
    activities = []

    for item in sample_arr:
        activity = create_activity(item)
        activities.append(activity)

    print(activities[0].name, activities[0].lat, activities[0].lon, activities[0].address)

    return activities

    # Function that fetches a list of activities near the location sent by user and returns three of them
def fetch_places(keyword):
    url = 'http://open-api.myhelsinki.fi/v1/places/?tags_search=' + keyword
    data = requests.get(url).json()
    results = data['data']
    sample_arr = results[:3]
    print(sample_arr)
    places = []

    for item in sample_arr:
        place = create_place(item)
        places.append(place)

    print(places[0].name, places[0].lat, places[0].lon, places[0].address)

    return places


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


# Function that fetches a list of all train stations abbrevations and full names
def fetch_stations():
    result = requests.get("https://rata.digitraffic.fi/api/v1/metadata/stations").json()
    station_codes_list = []
    for item in result:
        print(item['stationName'] + ', ' + item['stationShortCode'])
        station_codes_list.append(item)
    return station_codes_list


# Function that fetches coordinates by address word from digitransit Geocoding API. Used to generate route plans.
def fetch_coords(address):
    result = requests.get("https://api.digitransit.fi/geocoding/v1/search?text=" + address + "&size=1").json()
    coordinates = []
    coordinates.append(result['features'][0]['geometry']['coordinates'][0])
    coordinates.append(result['features'][0]['geometry']['coordinates'][1])
    return coordinates


# Function that fetches all events from Helsinki open API and returns the events as a list
def fetch_all():
    def get_event_name(item):
        return item.name
      
    # Function to help filter out events that have no start time
    def filter_events_with_starttime(item):
        if item['event_dates']['starting_day'] is None:
            return False
        else:
            return True

    url = "http://open-api.myhelsinki.fi/v1/events/"
    data = requests.get(url).json()
    all_events = data['data']
    all_events = filter(filter_events_with_starttime, all_events)

    events = []
    event_names = []
    for item in all_events:
        event = create_event(item)
        if event.name not in event_names:
            events.append(event)
            event_names.append(event.name)
        else:
            event_to_add_st = next((x for x in events if x.name == event.name), None)
            event_to_add_st.add_start_time(event.start_time[0])

    # sort alphabetically
    # events.sort(key=get_event_name)

    return events


# This function fetches all events from myHelsinki-api and filters items on a given day
def fetch_by_date(events, date):
    def filter_events(item):
        if str_to_datetime(date).date() in item.get_start_dates():
            return True
        else:
            return False

    sample_array = filter(filter_events, events)

    events = []
    for item in sample_array:
        print(item.name)
        events.append(item)
        if len(events) >= 3:
            break
    return events
