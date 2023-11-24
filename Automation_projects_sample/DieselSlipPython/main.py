from datetime import datetime
from time import sleep


import Modules.loginPage as loginPage
from config import dieselSlipSearchURL, errorEmailTo, plantLocation, branchSelectionURLPage, waitBetweenRepeat
from Modules.browserFunctionality import getBrowserElement
from Modules.fetchData import getLRData
from Modules.fillDieselSlipForm import generateDieselSlip
from Modules.locaters import (branchSelector, homeMenuOptionSelector,
                              lastSlipTime)
from Utilities.sendEmail import sendMail
from Utilities.logger import log


def dieselSlip(browser):

    log("info", "Start of Diesel Slip")
    
    loginPage.login(browser)
    
    if(not loginPage.isLoggedIn(browser)):
        raise Exception("Unable to login user!")
    while(1):
        for plant in plantLocation:
            log("info", "Working on plant : " + plant)
            browser.get(branchSelectionURLPage)
            browser.find_element_by_xpath(branchSelector.replace("<BRANCH>", plant)).click()
            browser.find_element_by_id(homeMenuOptionSelector).click()
            
            data = getLRData(browser)

            for value in data:
                try:
                    browser.get(dieselSlipSearchURL.replace("<VEHICLENO>", value.get("vehicleNo")))
                    lastDieselSlipTime = datetime.strptime(browser.find_element_by_xpath(lastSlipTime).text, "%d/%m/%Y %H:%M")
                    if(lastDieselSlipTime < value.get("time")):
                        generateDieselSlip(browser,value, plant)
                except Exception as exception:
                    log("ERROR", str(exception))
                    sendMail(errorEmailTo,"Failed to generate Diesel Slip for vehcile no :- %s"%(value.get("vehicleNo")),str(exception))
            sleep(waitBetweenRepeat)
    
    log("info","End of Diesel Slip FUnction")

def main():
    browser =  getBrowserElement()
    try:
        dieselSlip(browser)
    except Exception as e:
        log("ERROR",str(e))
        sendMail(errorEmailTo,"Could not generate diesel slip",str(e))
    finally:
        if(browser):
            browser.close()

main()
