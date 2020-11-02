from classes.Train import Train
from utilities import str_to_datetime

# --- HERE WE FORM TRAIN OBJECTS FROM FETCHED DATA ---


# Function to create an instance of Train
def create_train(item):
    train = Train()

    train.number = item['trainNumber']
    train.datetime = str_to_datetime(item['timeTableRows'][0]['scheduledTime'])
    train.train_type = item['trainType']
    train.train_category = item['trainCategory']
    train.line_id = item['commuterLineID']
    train.departure = item['timeTableRows'][0]['stationShortCode']
    train.arrival = item['timeTableRows'][-1]['stationShortCode']
    train.fromTrack = item['timeTableRows'][0]['commercialTrack']
    train.toTrack = item['timeTableRows'][-1]['commercialTrack']
    return train
