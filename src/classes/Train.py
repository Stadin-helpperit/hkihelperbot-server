# Class for each train fetched from VR API, used to create timetable info

class Train:
    def __init__(self, number='', datetime='', train_type='', train_category='', line_id='', departure='', arrival='',
                 fromTrack='', toTrack=''):
        self.number = number
        self.datetime = datetime
        self.train_type = train_type
        self.train_category = train_category
        self.line_id = line_id
        self.departure = departure
        self.arrival = arrival
        self.fromTrack = fromTrack
        self.toTrack= toTrack