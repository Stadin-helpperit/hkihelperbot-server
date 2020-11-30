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
![Python package](https://github.com/Stadin-helpperit/hkihelperbot-server/workflows/Python%20package/badge.svg)
![CodeQL](https://github.com/Stadin-helpperit/hkihelperbot-server/workflows/CodeQL/badge.svg)
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="imgs/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Helsinki Helper Bot</h3>

  <p align="center">
    Helsinki Helper is a chatbot in the Telegram messaging app that utilizes open data from the 
    [MyHelsinki Open API](http://open-api.myhelsinki.fi/). The bot responds to different commands and requests. 
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
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
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
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This telegram bot was developed by Daniel Buselli, Feeliks Kilpi, Nikolas Kunnas, Juho Toivonen, Henri Väisänen 
on [Haaga-Helia's](https://www.haaga-helia.fi/fi) [software project II](https://opinto-opas.haaga-helia.fi/course_unit/SWD4TA024) course.


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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

![gif](/imgs/search.gif)

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

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email
Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email
Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email
Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email
Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/Stadin-helpperit/hkihelperbot-server](https://github.com/Stadin-helpperit/hkihelperbot-server)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/Stadin-helpperit/hkihelperbot-server/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt