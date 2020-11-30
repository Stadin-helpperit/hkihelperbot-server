import requests
from datetime import datetime

# To be used as parameters for query to get the response for today and now
today_date = datetime.today().strftime('%Y-%m-%d')
today_time = datetime.now().strftime("%H:%M:%S")

# --- This is to fetch HSL Routing API data with GraphQL ---


def fetch_hsl_route(from_loc, to_loc):
    headers = {'Content-Type': 'application/json'}
    query = """
    {
      plan(
        fromPlace: """ + '"' + from_loc + '"' + """,
        toPlace: """ + '"' + to_loc + '"' + """,
        date: """ + '"' + today_date + '"' + """,
        time: """ + '"' + today_time + '"' + """,
      ) {
        itineraries{
          walkDistance,
          duration,
          legs {
            mode
            startTime
            endTime
            from {
              lat
              lon
              name
              stop {
                code
                name
              }
            },
            to {
              lat
              lon
              name
            },
            distance
            legGeometry {
              length
              points
            },
            route {
              shortName
              longName
            }
          },
          fares {
            type
            cents
            currency
          }
        }
      }
    }
    """

    request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# This function uses the digitransit address search api to find coordinates for user inputted places
def fetch_search_address(place_name):
    url = 'https://api.digitransit.fi/geocoding/v1/search?text={}&size=1'.format(place_name)
    data = requests.get(url).json()
    # extract coords and label from data
    coords = {'lon': data['features'][0]['geometry']['coordinates'][0],
              'lat': data['features'][0]['geometry']['coordinates'][1]}
    label = data['features'][0]['properties']['label']

    # change to the format used by digitransit graphql routing api
    address_and_loc = label + '::' + str(coords['lat']) + ' ' + str(coords['lon'])

    return address_and_loc


def create_route_msg(hsl_fetch_result):
    # converts timestamp data to string
    def timestamp_to_string(ts):
        dt = datetime.fromtimestamp(int(ts / 1000))
        dt_str = dt.strftime("%H:%M")
        return dt_str

    # creates the appropriate message for each mode of transport
    def create_submsg_for_mode(leg):
        submsg = ''
        duration = str(round(((leg['endTime'] - leg['startTime']) / 1000 / 60)))
        if leg['mode'] == 'WALK':
            submsg += 'Walk {} m ({} min)'.format(str(int(round(leg['distance'], -1))), duration)
        elif leg['mode'] == 'BUS':
            submsg += 'Take the bus {} ({} min)'.format(leg['route']['shortName'], duration)
        elif leg['mode'] == 'SUBWAY':
            metro_suunta = leg['route']['longName'].split(' - ')[1]
            submsg += 'Take the metro to direction {} ({} min)'.format(metro_suunta, duration)
        elif leg['mode'] == 'RAIL':
            submsg += 'Take the {}-train ({} min)'.format(leg['route']['shortName'], duration)
        elif leg['mode'] == 'TRAM':
            submsg += 'Take the tram {} ({} min)'.format(leg['route']['shortName'], duration)
        elif leg['mode'] == 'FERRY':
            submsg += 'Take the ferry {} ({} min)'.format(leg['route']['shortName'], duration)
        else:
            submsg += leg['mode']

        return submsg

    # First route suggestion to be used only
    legs = hsl_fetch_result['data']['plan']['itineraries'][0]['legs']
    route_msg = ''
    i = 1

    # basic information about the route
    route_duration = hsl_fetch_result['data']['plan']['itineraries'][0]['duration'] / 60

    if route_duration < 60:
        route_duration = str(int(route_duration)) + ' min'
    else:
        route_duration = str(route_duration // 60) + ' h, ' + str(route_duration % 60) + ' min'

    route_msg += '<b>Duration of trip: </b>' + route_duration
    route_msg += '\n<b>Walk distance: </b>' + \
                 str(int(round(hsl_fetch_result['data']['plan']['itineraries'][0]['walkDistance'], -1))) + ' metriä'
    route_msg += '\n<b>Total price: </b>' + \
                 "{:.2f}".format(hsl_fetch_result['data']['plan']['itineraries'][0]['fares'][0]['cents'] / 100) + ' €\n\n'

    # first leg of the journey
    route_msg += '<b>' + legs[0]['from']['name'] + '</b>' + '\t' + timestamp_to_string(legs[0]['startTime'])
    route_msg += '\n ·\n · {} \n ·\n'.format(create_submsg_for_mode(legs[0]))

    # other legs
    while i in range(len(legs)):
        route_msg += '<b>' + legs[i]['from']['name'] + '</b>' + '\t' + timestamp_to_string(legs[i]['startTime'])
        route_msg += '\n ·\n · {} \n ·\n'.format(create_submsg_for_mode(legs[i]))
        i += 1

    # last leg
    route_msg += '<b>' + legs[-1]['to']['name'] + '</b>' + '\t' + timestamp_to_string(legs[-1]['endTime'])

    return route_msg
