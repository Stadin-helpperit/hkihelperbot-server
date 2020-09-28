# hkihelperbot-server

### This branch is used to develop the master branch bot so that it consists of smaller Python modules instead of a singular file

Stadin Helpperit Telegram bot is a chatbot in the Telegram messaging app that utilizes open data from the [MyHelsinki Open API](http://open-api.myhelsinki.fi/).
The bot responds to different commands and requests. 

Try it out: [@HelsinkiHelperBot](https://t.me/HelsinkiHelperBot) (link to try the bot on Telegram web / local client)

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
