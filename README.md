# NBA Player Statistics Engine

This desktop app allows the user to input an NBA player's name, an the engine will return his picture and his career per-game statistics.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install:

1. BeautifulSoup data scraper
```bash
pip install beautifulsoup4
```

2. CustomTkInter UI-Library
```bash
pip install customtkinter
```

3. Requests, Validators, urllib modules
```bash
pip install requests
pip install validators
pip install urllib3
```


The remaining modules are part of Python's standard library, so they do not need to be installed.

## Usage
When the user enters a valid NBA player's name, the backend will scrap the data from BasketballReference.com for his career statistics as well as download and display an image of the player. Therefore, the image folder will contain .jpg files scraped from the html file.

## Contributing

You are welcome to download and play around with this app. Any feedback is encouraged.
