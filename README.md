<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Python package][python-shield]][actions-url]
[![CodeQL][code-shield]][actions-url]
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Stadin-helpperit/hkihelperbot-server/">
    <img src="imgs/logo.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Helsinki Helper Bot</h3>

  <p align="center">
    Helsinki Helper is a chatbot in the Telegram messaging app that utilizes open data from the 
    <a href="http://open-api.myhelsinki.fi/">MyHelsinki Open API</a>. The bot responds to different commands and requests. 
    <br />
    <a href="https://github.com/Stadin-helpperit/hkihelperbot-server"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Stadin-helpperit/hkihelperbot-server">View Demo</a>
    ·
    <a href="https://github.com/Stadin-helpperit/hkihelperbot-server/issues">Report Bug</a>
    ·
    <a href="https://github.com/Stadin-helpperit/hkihelperbot-server/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<img src="/imgs/helperss1.png" width="800" alt="Screenshot of project"/>

This [Telegram bot](https://core.telegram.org/bots) was developed by Daniel Buselli, Feeliks Kilpi, Nikolas Kunnas, Juho Toivonen and Henri Väisänen 
on [Haaga-Helia's](https://www.haaga-helia.fi/fi) [software project II](https://opinto-opas.haaga-helia.fi/course_unit/SWD4TA024) course.

The bot is designed to help tourists in Helsinki find interesting things to do by utilizing the data from [MyHelsinki Open API](http://open-api.myhelsinki.fi/).
To make useage as quick and easy as possible the bot uses Telegrams's inline keyboard functionality to have a dialouge with the user about preferences 
before querying the API and outputting the data in an easy to read format.

Try it out: [@HelsinkiHelperBot](https://t.me/HelsinkiHelperBot) (link to try the bot on Telegram web / local client, it's probably not running though :disappointed:)

##### Currently supported commands

- /search [keyword] -- Search for events, places and activites in Helsinki
- /searchdate -- Search for events on a specific day
- /from [start address] to [destination address] -- Returns public transport directions to the destination
- /trains [stationcode] -- Returns arriving and departing trains from the specified station
- /weather -- returns current local weather in Helsinki
- /help -- Shows the help text that shows up when you first start the bot

##### Other functionality

- You can send your location (or any location) through Telegram's attachment menu and receive up to 3 events nearby the sent location.

### Built With

* [Python](https://www.python.org/)
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [MyHelsinki Open API](http://open-api.myhelsinki.fi/)
* [OpenWeatherMap](https://openweathermap.org/api)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

What you need on your machine to get this running.
* Python, install from [https://www.python.org/downloads/](https://www.python.org/downloads/) or if you're on Linux
feel free to use your preferred package manager.

### Installation

Tested to work in Python 3.6, 3.7 and 3.8. Built with Python 3.8.

Clone the repository to your machine:
>`git clone https://github.com/Stadin-helpperit/hkihelperbot-server.git`
>
Install the dependencies:
>`pip install -r requirements.txt`
>
Now you need to make a .env file for your environment variables and add your Telegram Bot API Key to there. You can use the following command, just replace <YOUR API KEY> with your own API key. You can get your own API key from Telegram's [@BotFather](https://t.me/BotFather).
>
>`echo API_TOKEN = "<YOUR API KEY>" > .env`
>
There's also a weather API token you need to add for the "/weather" command to work. We've used [OpenWeatherMap](https://openweathermap.org/api).
If you use another weather API you'll likely need to edit the code a bit to make it work.
>
>`echo WeatherApi_TOKEN = "<YOUR API KEY>" > .env`
>
Now you can run the app with the following command:
>`python bot.py`



<!-- USAGE EXAMPLES -->
## Usage

You use the bot by typing in commands. You can check the available commands with the `/help` command. The telegram bot we use for production ([@HelsinkiHelperBot](https://t.me/HelsinkiHelperBot))
will also help you by showing you the available commands as you type.

Below you can see the `/search` command in use.

<img src="/imgs/search.gif" width="300" alt="GIF of search function"/>

### Generally helpful code for other Telegram bots written in Python

Check out ```tag_keyboard_util.py``` in the src folder and the functions ```handle_search_events()``` and ```handle_search_places()``` in ```bot.py``` for how we dynamically create the search keyword/tag inline keyboard based on the data in ```tag_keyboard.json```. You can see this code in action on the gif above!

We also used [telegram-calendar-keyboard](https://github.com/grcanosa/telegram-calendar-keyboard) by [grcanosa](https://github.com/grcanosa) to create the calendar for the bot's /searchdate function.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Stadin-helpperit/hkihelperbot-server/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Daniel Buselli, Feeliks Kilpi, Nikolas Kunnas, Juho Toivonen and Henri Väisänen

Project Link: [https://github.com/Stadin-helpperit/hkihelperbot-server](https://github.com/Stadin-helpperit/hkihelperbot-server)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/github/workflow/status/Stadin-helpperit/hkihelperbot-server/Python%20package?style=for-the-badge
[code-shield]: https://img.shields.io/github/workflow/status/Stadin-helpperit/hkihelperbot-server/CodeQL?label=CodeQL&style=for-the-badge
[actions-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/actions
[contributors-shield]: https://img.shields.io/github/contributors/Stadin-helpperit/hkihelperbot-server.svg?style=for-the-badge
[contributors-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/Stadin-helpperit/hkihelperbot-server.svg?style=for-the-badge
[issues-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/issues
[license-shield]: https://img.shields.io/github/license/Stadin-helpperit/hkihelperbot-server?style=for-the-badge
[license-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/blob/master/LICENSE
