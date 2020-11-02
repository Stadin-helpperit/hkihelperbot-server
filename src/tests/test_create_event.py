import json
from ..create_event import create_event

with open("./test_events.json") as jsonfile:
    data = json.load(jsonfile)


def test_create_event_nameless():
    test_event = create_event(data[0])
    assert test_event.name == 'Ei ilmoitettua nimeä'


def test_create_event_no_url_link():
    test_event = create_event(data[1])
    assert test_event.link is None


def test_create_event_no_location():
    test_event = create_event(data[2])
    assert test_event.lat is None and test_event.lon is None


def test_create_event_no_tags():
    test_event = create_event(data[3])
    assert test_event.tags == 'Tapahtumalla ei tageja'


def test_create_event_no_address():
    test_event = create_event(data[4])
    assert test_event.address == 'Ei ilmoitettua osoitetta'


def test_create_event_no_dates():
    test_event = create_event(data[5])
    assert test_event.start_time == 'Ei ilmoitettua aloituspäivämäärää' and test_event.end_time == 'Ei ilmoitettua lopetuspäivämäärää'


def test_create_event_no_image():
    test_event = create_event(data[6])
    assert test_event.img_link is None
