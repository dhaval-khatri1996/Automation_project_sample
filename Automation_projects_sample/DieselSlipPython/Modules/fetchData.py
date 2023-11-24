from config import (LRSearchURL)
from datetime import datetime,timedelta
from Modules.locaters import LRListDataRow, LRlistDataColumn
from Utilities.logger import log
import time

def getLRData(browser):
    log("info", "getLRData start")
    yesterday = (datetime.today() - timedelta(1)).strftime("%d/%m/%Y")
    dataURL =  LRSearchURL.replace("<FROMDATE>",yesterday).replace("<TODATE>",datetime.today().strftime("%d/%m/%Y"))
    browser.get(dataURL)
    return scrapData(browser)



def scrapData(browser):
    log("info","scrap data start")
    data = []
    numberOfRows = len(browser.find_elements_by_xpath(LRListDataRow)) -2
    for i in range(2,numberOfRows+1,+1):
        tempLocator = LRlistDataColumn.replace("indexRow",str(i))
        record = {}
        record["LRId"] = browser.find_element_by_xpath(tempLocator.replace("index","1")).text
        record["time"] = datetime.strptime(browser.find_element_by_xpath(tempLocator.replace("index","2")).text,"%d/%m/%Y %H:%M")
        record["fromStation"] = browser.find_element_by_xpath(tempLocator.replace("index","7")).text
        record["toStation"] = browser.find_element_by_xpath(tempLocator.replace("index","8")).text
        record["vehicleNo"] = browser.find_element_by_xpath(tempLocator.replace("index","9")).text
        
        data.append(record)
    
    return data