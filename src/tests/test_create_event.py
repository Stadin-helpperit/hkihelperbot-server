import json
from pathlib import Path
from create_event import create_event

path = Path(__file__).parent / "./test_events.json"

with open(path) as jsonfile:
    data = json.load(jsonfile)


def test_create_event_nameless():
    test_event = create_event(data[0])
    assert test_event.name == 'No name announced'


def test_create_event_no_url_link():
    test_event = create_event(data[1])
    assert test_event.link is None


def test_create_event_no_location():
    test_event = create_event(data[2])
    assert test_event.lat is None and test_event.lon is None


def test_create_event_no_tags():
    test_event = create_event(data[3])
    assert test_event.tags == ['The event has no tags']


def test_create_event_no_address():
    test_event = create_event(data[4])
    assert test_event.address == 'No address announced'


def test_create_event_no_dates():
    test_event = create_event(data[5])
    assert test_event.start_time == 'No starting date announced' and test_event.end_time == 'No ending date announced'


def test_create_event_no_image():
    test_event = create_event(data[6])
    assert test_event.img_link is None
