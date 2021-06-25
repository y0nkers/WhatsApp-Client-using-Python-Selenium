# WhatsApp-Client-using-Python-Selenium
Simple WhatsApp client developed in python using Selenium Webdriver. The client can send messages, documents and media files using web.whatsapp.com

## Features

- Sending and receiving messages
- Sending voice messages
- Sending documents and media files
- Sending contacts from your phone book
- Sending emoji
- Sending smiles ASCII art

## Requirements

* [Python 3+]
* [Selenium](https://github.com/SeleniumHQ/selenium) - Selenium for web automation
* [ChromeDriver](https://chromedriver.chromium.org/downloads) - Latest version of WebDriver for Chrome
* Latest Chrome version

P.S. The application was tested on Chrome version 90

## Files

- app.py - Main file.
- dependencies.py - File with all the necessary dependencies and a config, which contains the paths to the ChromeDriver and the chrome data directory.
- modules.py - File with all functions for the client's work.
- smiles.py - File with smiles in the form of ASCII art

## Launching

First of all, in dependencies.py you must change the variables for the WebDriver storage folder and the path to chromedriver.exe in config.

When you run app.py, you must scan the appeared QR-code in the WhatsApp mobile application. 

In order not to scan the code every time, the Chrome Data Directory is used. If it gets too big, you can delete it.

When the code is scanned, type Ok or just press Enter. Next, enter the name of contact. For a list of available commands, write help.

## Problems 

- Some functions (e.g. sending a contact) work half the time, I don't know why =(
- Some elements of the site (e.g., the send button) have different names in light and dark mode, so the client may not work if the site is in light mode. Use dark mode for correct work.
- Bad implementation of smiles, they look good on PC version, but bad on mobile.
