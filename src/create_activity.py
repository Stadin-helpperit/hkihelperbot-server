from classes.Activity import Activity

def create_activity(item):

     # Create an empty activity
    activity = Activity()

    # Set the English name for the activity and if it doesn't exist choose the Finnish name
    if item['name']['en'] is not None:
        activity.name = item['name']['en']
    elif item['name']['fi'] is not None:
        activity.name = item['name']['fi']
    else:
        activity.name = 'Ei ilmoitettua nimeä'

    # Set the address if it exists
    if item['location']['address']['street_address'] is not None:
        activity.address = item['location']['address']['street_address']
    else:
        activity.address = 'Ei ilmoitettua osoitetta'


    # Set coordinates for the activity
    activity.lat = item['location']['lat']
    activity.lon = item['location']['lon']

    # Set the description of the activity
    if item['description']['body'] is None:
        activity.desc = 'Kuvausta ei saatavilla'
    else:
        activity.desc = item['description']['body']

    # Set the info link url of the activity
    activity.link = item['info_url']

    # Set the tags for the activity from list
    if len(item['tags']) < 1:
        activity.tags = ['Tapahtumalla ei tageja']
    else:
        tags = item['tags']
        for tag in tags:
            activity.add_tag(tag['name'])

    # Set image if it exists
    if item['description']['images']:
        if item['description']['images'][0]['url'] is not None and '{' not in item['description']['images'][0]['url']:
            activity.img_link = item['description']['images'][0]['url'] 

    # Where the activity happens and when 
    # How long the activity lasts
    activity.where_and_when = item['where_when_duration']['where_and_when']
    activity.duration = item['where_when_duration']['duration']



    # Return the created activity
    return activity