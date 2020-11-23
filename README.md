# hkihelperbot-server ![Python package](https://github.com/Stadin-helpperit/hkihelperbot-server/workflows/Python%20package/badge.svg) ![CodeQL](https://github.com/Stadin-helpperit/hkihelperbot-server/workflows/CodeQL/badge.svg)

Stadin Helpperit Telegram bot is a chatbot in the Telegram messaging app that utilizes open data from the [MyHelsinki Open API](http://open-api.myhelsinki.fi/).
The bot responds to different commands and requests. 

Try it out: [@HelsinkiHelperBot](https://t.me/HelsinkiHelperBot) (link to try the bot on Telegram web / local client)

##### Currently supported commands

- /search [keyword] -- Search for events, places and activites in Helsinki
- /searchdate -- Search for events on a specific day
- /trains [stationcode] -- Returns arriving and departing trains from the specified station

##### Other functionality

- You can send your location (or any location) through Telegram's attachment menu and receive up to 3 events nearby the sent location.

## Technologies

The bot is written in Python and it will be hosted on a Raspberry Pi server. 

## How to install?

Clone this repository and open a terminal window in a location you wish to have the project in. Then run Bot.py.

You'll need Python 3.8.5.

Cloning the repository to your machine:
>`git clone https://github.com/Stadin-helpperit/hkihelperbot-server.git`
>
Installing the dependencies:
>`pip install -r requirements.txt`
>
Now you need to make a .env file for your environment variables and add your Telegram Bot API Key to there. You can use the following command, just replace <YOUR API KEY> with your own API key. You can get your own API key from Telegram's [@BotFather](https://t.me/BotFather).
>
>`echo API_TOKEN = "<YOUR API KEY>" > .env`
>
Now you can run the app with the following command:
>`python bot.py`
