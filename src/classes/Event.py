# Universal class for blank event to be used to create instances of events

class Event:
    def __init__(self, name='', lat=0.0, lon=0.0, address='', desc='', end_time='', link=None,
                 img_link=None):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.desc = desc
        self.start_time = []
        self.end_time = end_time
        self.tags = []
        self.link = link
        self.img_link = img_link

    def add_start_time(self, start_time):
        self.start_time.append(start_time)

    def add_tag(self, tag):
        self.tags.append(tag)
