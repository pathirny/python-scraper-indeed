import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
url = "https://uk.indeed.com/jobs?q=junior+software+engineer&l=London%2C+Greater+London&from=searchOnHP&vjk=6f2091c334c10398"

response = requests.get(url, headers=Headers)
print(response.status_code)

