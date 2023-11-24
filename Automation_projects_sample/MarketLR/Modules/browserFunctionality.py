from selenium import webdriver
from config import waitTime,driverPath
from Utilities.logger import log

def getBrowserElement():
    log("info","fetching webdriver")
    browser = webdriver.Chrome(driverPath)
    browser.implicitly_wait(waitTime)
    return browser