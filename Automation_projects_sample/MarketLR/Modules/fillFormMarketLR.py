from datetime import datetime
from time import sleep

from config import loadingSupervisorName, vehicleRelasedBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from Utilities.logger import log

import Modules.locaters as locaters


def fill(browser,data):
    
    log("info", "start of fill data: %s"%data)
    browser.find_element_by_id(locaters.CNNoInput).send_keys(data.get("CN NO."))
    
    browser.find_element_by_id(locaters.CNRefDateInput).send_keys(datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    browser.find_element_by_xpath(locaters.CustomerNameSelect.replace("<CUSTOMERNAME>", data.get("CUSTOMER NAME"))).click()
    
    try:
        browser.find_element_by_id(locaters.DINoInput).send_keys(data.get("DI NO"))
    except:
        browser.find_element_by_id(locaters.DINoInput).send_keys(data.get("DI NO"))
    
    browser.find_element_by_id(locaters.vehicleNoInput).send_keys(data.get("VEHICLE NO"))
    
    
    browser.find_element_by_xpath(locaters.loadingSupervisorNameSelect.replace("<LOADINGSUPERVISORNAME>", loadingSupervisorName)).click( )
    
    browser.find_element_by_xpath(locaters.fromStationSelect.replace("<FROMSTATION>", data.get("FROM STATION(CONSIGNER)"))).click()
    
    sleep(3)
    browser.find_element_by_xpath(locaters.toStationSelect.replace("<TOSTATION>", data.get("TO STATION(CONSIGNEE)"))).click()
    
    route = "--Select--"
    #route = data.get("FROM STATION(CONSIGNER)") + "-" + data.get("TO STATION(CONSIGNEE)")
    browser.find_element_by_xpath(locaters.routeSelect.replace("<ROUTE>",route)).click()

    #material details
    browser.find_element_by_id(locaters.EGPNumberInput).send_keys(data.get("EGP NO. (INVOICE NUMBER)"))
    
    EGPdate = datetime.strptime(data.get("EGP DATE & TIME"),"%d-%b-%Y").strftime("%d/%m/%Y")
    browser.find_element_by_id(locaters.EGPDateTimeInput).send_keys(str(EGPdate) + " 00:000")
    
    browser.find_element_by_id(locaters.productNameSelect).send_keys(data.get("PRODUCT NAME"))
    
    browser.find_element_by_xpath(locaters.freightOnSelect.replace("<FREIGHTON>","On Gross Weight")).click()
    
    browser.find_element_by_id(locaters.noOfPackagesInput).send_keys(data.get("NUMBER OF PACKAGES"))
    
    browser.find_element_by_id(locaters.materialTypeSelect).send_keys(data.get("PIECES/BUNDLES/PACKING TYPE"))
    
    browser.find_element_by_id(locaters.grossRateInput).send_keys(data.get("GROSS RATE"))
    
    browser.find_element_by_id(locaters.netRateInput).send_keys(data.get("GROSS RATE"))
    
    browser.find_element_by_xpath(locaters.UOMSelect.replace("<UOM>","MT")).click()
    
    browser.find_element_by_id(locaters.netWeightInput).send_keys(data.get("NET WT."))
    
    browser.find_element_by_id(locaters.addMaterialDetailsButton).click()
    

    #misc
    browser.find_element_by_xpath(locaters.vehicleReleasedBySelect.replace("<VEHICLERELEASEDBY>",vehicleRelasedBy)).click()
    

    browser.find_element_by_id(locaters.saveButton).click()

    try:
        WebDriverWait(browser, 3).until(expected_conditions.alert_is_present(),"waiting for alert message")
        alert = browser.switch_to.alert
        alertText = alert.text 
        alert.accept()
        log("info","alert accepted : "+ alertText)
        raise Exception(alertText)
    except TimeoutException:
        log("info", "no alert")

    message = browser.find_element_by_id(locaters.statusForLREntry).text
    log("info", message)
    log("info", "End of fill function")
    
