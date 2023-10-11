"""
Webscraping Project for Swiss Amateur Soccer
============================================

web_driver.py
----------
Initialize chrome webdriver for selenium

"""

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--headless")

driver = webdriver.Chrome(
    r"C:\Python39\chromedriver_win32\chromedriver.exe", options=options
)

