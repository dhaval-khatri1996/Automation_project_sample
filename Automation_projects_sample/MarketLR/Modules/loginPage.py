import Modules.locaters as locaters
import config as config
from Utilities.logger import log


def login(browser):
    log("info","login user to ERP")
    browser.get(config.loginURL)
    browser.find_element_by_id(locaters.usernameInput).send_keys(config.username)
    browser.find_element_by_id(locaters.passwordInput).send_keys(config.password)
    browser.find_element_by_id(locaters.loginButton).click()

def isLoggedIn(browser):
    currentURL = browser.current_url
    if(config.loginURL == currentURL ):
        log("Warning","Unable to loggin USER. Check Username/password and try again")
        return False
    return True