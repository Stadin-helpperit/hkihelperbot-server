# hkihelperbot-server

Stadin Helpperit Telegram bot is a chatbot in the Telegram messaging app aimed to utilize open data from the [MyHelsinki Open API](http://open-api.myhelsinki.fi/).
The bot answers to different commands and requests. 

##### Currently supported commands

- /search [keyword] -- Sends back events that match the keywords.

##### Other functionality

- You can send your location (or any location) through Telegram's attachment menu and receive up to 3 events nearby the sent location.

## Technologies

The bot is written in Python and it will be hosted on a Raspberry Pi server. 

## How to use?

Clone this repository and open a terminal window in a location you wish to have the project in. Then run Bot.py.

>`git clone https://github.com/Stadin-helpperit/hkihelperbot-server.git`
>
>`python bot.py`
