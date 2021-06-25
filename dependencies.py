import sched
import sys
import threading
import time
import os

from random import seed, choice
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

config = {
    'chrome_data_directory': "D:/project/Python/WhatsApp/Data",  # Папка для хранения данных вебдрайвера
    'path_to_chromedriver': "D:/project/Python/WhatsApp/chromedriver.exe",  # Путь до chromedriver.exe
    'get_message_interval': 5,  # Интервал для проверки на новые сообщения.
    'whatsapp_url': "https://web.whatsapp.com/"  # URL WhatsApp
}

incoming_scheduler = sched.scheduler(time.time, time.sleep)
receiver_name = ''
last_printed_message = None
stopsending = -1
