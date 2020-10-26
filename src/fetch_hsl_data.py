import requests
import pytz
from datetime import datetime, timedelta

# To be used as parameters for query to get the response for today and now
today_date = datetime.today().strftime('%Y-%m-%d')
today_time = datetime.now().strftime("%H:%M:%S")

# --- This is to fetch HSL Routing API data with GraphQL ---

def fetch_hsl_route():
    headers = {'Content-Type': 'application/json'}
    query = """
    {
      plan(
        fromPlace: "Kamppi, Helsinki::60.168992,24.932366",
        toPlace: "Käpylä, Helsinki::60.212568, 24.956627",
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

# Whole response array
result = fetch_hsl_route()
# First route suggestion to be used only
scope = result['data']['plan']['itineraries'][0]['legs']

def create_route_msg():
    # list for different steps in route plan
    route_a = []
    # list for start times for route parts
    start_times = []
    # list for end times for route parts
    end_times = []
    # price of the whole trip
    fare = int(result['data']['plan']['itineraries'][0]['fares'][0]['cents'])
    steps = []

    for i in range(len(scope)):
        # from place name
        a = str(scope[i]['from']['name'])
        # to place name
        b = str(scope[i]['to']['name'])

        start_times.append(str(scope[i]['startTime']))
        end_times.append(str(scope[i]['endTime']))


        if scope[i]['route'] is not None:
            # Route name means bus/rail etc line number
            route_a.append(str(scope[i]['route']['shortName']))
        else:
            route_a.append('kävely')

        steps.append(str('Part of the trip, at: ' + start_times[i] + ' from place: ' + a + ' To: ' + b + ' at: ' + end_times[i] + ' - kulkuvälineellä: ' + route_a[i]))

    # print(result)
    steps.append(str('Matkan kokonaishinta: ' + str(fare / 100) + ' Euroa'))

    return steps

