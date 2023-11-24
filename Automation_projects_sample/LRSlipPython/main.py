from os import listdir, rename
from os.path import isfile, join

import Modules.loginPage as loginPage
from config import (URLToLR, branchSelectionURLPage, errorEmail,
                    inputFolderPath, plantLocation, folderPathToFailedLR, folderPathToSuccessfullLR)
from Modules.browserFunctionality import getBrowserElement
from Modules.fillFormMarketLR import fill
from Modules.locaters import branchSelector
from Utilities.formatInputData import generateMap
from Utilities.logger import log
from Utilities.sendEmail import sendMail


def LRProcess(browser):
      
    loginPage.login(browser)
    if(not loginPage.isLoggedIn(browser)):
        raise Exception("Unable to login user!")
    for plant in plantLocation:
        log("Info", "working on plant :" + plant)
        try:
            browser.get(branchSelectionURLPage)
            browser.find_element_by_xpath(branchSelector.replace("<BRANCH>", plant)).click()
            folderPath = inputFolderPath.get(plant)
            onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
            for file in onlyfiles:
                data = generateMap(join(folderPath,file))
                browser.get(URLToLR)
                try:
                    log("info","found market vehicle.")
                    fill(browser,data, plant)
                    rename(join(folderPath,file),join(folderPathToSuccessfullLR,file))
                except Exception as e:
                    rename(join(folderPath,file),join(folderPathToFailedLR,file))
                    log("ERROR", str(e))
                    sendMail(errorEmail, "Market LR process Failed", str(e))
        except Exception as e:
            log("ERROR", str(e))
            sendMail(errorEmail, "Market LR process Failed", str(e))



def main():
    browser =  getBrowserElement()
    try:
        LRProcess(browser)
    except Exception as e:
        print(e)
    finally:
        if(browser):
            browser.close()
        
main()
