# Universal class for Place instances in Helsinki API

class Place:
    def __init__(self, name='', address='', desc='', lat=0.0, lon=0.0, link=None, img_link=None):
        self.name = name
        self.address = address
        self.desc = desc
        self.lat = lat
        self.lon = lon
        self.open_hours = []
        self.tags = []
        self.link = link
        self.img_link = img_link

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_open_hours(self, weekday):
        self.open_hours.append(weekday)
