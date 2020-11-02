# Universal class for blank event to be used to create instances of events

class Activity:
    def __init__(self, name='', lat=0.0, lon=0.0, address='', desc='', link=None,
                 img_link=None, where_and_when='', duration=''):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address
        self.desc = desc
        self.tags = []
        self.link = link
        self.img_link = img_link
        self.where_and_when = where_and_when
        self.duration = duration
# myöhemmin opening hours

    def add_tag(self, tag):
        self.tags.append(tag)




   