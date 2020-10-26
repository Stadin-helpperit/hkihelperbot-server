from datetime import datetime
from classes.Train import Train
import pytz


# Helper functions to reformat date/time data
def str_to_datetime(date_string):
    date_time_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    from_zone_utc = pytz.utc
    to_zone_local = pytz.timezone("Europe/Helsinki")
    date_time_object = date_time_object.replace(tzinfo=from_zone_utc)
    date_time_object = date_time_object.astimezone(to_zone_local)
    return date_time_object


def datetime_to_str(date_time_object):
    if isinstance(date_time_object, datetime):
        date_string = date_time_object.strftime("%d.%m.%Y, %H:%M")
    else:
        date_string = date_time_object
    return date_string


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
