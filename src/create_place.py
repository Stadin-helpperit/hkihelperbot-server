from classes.Place import Place


def create_place(item):
    # Create an empty place
    place = Place()

    # Set the English name for the activity and if it doesn't exist choose the Finnish name
    if item['name']['en'] is not None:
        place.name = item['name']['en']
    elif item['name']['fi'] is not None:
        place.name = item['name']['fi']
    else:
        place.name = 'No name announced'

    # Set the address if it exists
    if item['location']['address']['street_address'] is not None:
        place.address = item['location']['address']['street_address']
    else:
        place.address = 'No address announced'

    # Set coordinates for the place
    place.lat = item['location']['lat']
    place.lon = item['location']['lon']

    # Set the description of the place
    if item['description']['body'] is None:
        place.desc = 'No description available'
    else:
        place.desc = item['description']['body']

    # Set the info link url of the place
    place.link = item['info_url']

    # Set the tags for the place from list
    if len(item['tags']) < 1:
        place.tags = ['Event has no tags']
    else:
        tags = item['tags']
        for tag in tags:
            place.add_tag(tag['name'].lower())

    # Set image if it exists
    if item['description']['images']:
        if item['description']['images'][0]['url'] is not None and '{' not in item['description']['images'][0]['url']:
            place.img_link = item['description']['images'][0]['url']

    # Return the created place
    return place
