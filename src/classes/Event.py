# Universal class for blank event to be used to create instances of events

class Event:
    def __init__(self, name='', lat=0.0, lon=0.0, address='', desc='', start_time='', end_time='', tags='', link=None,
                 img_link=None):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.desc = desc
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags
        self.link = link
        self.img_link = img_link
