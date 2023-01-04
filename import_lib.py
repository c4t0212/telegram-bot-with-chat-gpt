import os
import sys
import json
import logging
import requests as req
from time import sleep
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv
from selenium import webdriver
# from pytube.cli import on_progress
from pytube import YouTube as Youtube
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
