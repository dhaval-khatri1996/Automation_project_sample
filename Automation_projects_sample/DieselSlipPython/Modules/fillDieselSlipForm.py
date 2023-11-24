from sys import exec_prefix
from Utilities import sendEmail
from Utilities.sendEmail import sendMail
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from config import (URL, onAccountForDeffrencialDiesel,
                    onAccountForDieselDefault, errorEmailTo,
                    remarkForDieselSlip, mappingSheetPath)
from Utilities.logger import log
import Modules.locaters as locaters
import re
import pylightxl as xl
import random


def generateDieselSlip(browser, data, location):
    
    log("info",("generateDieselSlip function (%s,%s)"%(str(browser),str(data))))

    browser.get(URL)
    browser.find_element_by_xpath(locaters.selectVehicleNo.replace("<VEHICLENO>",data.get("vehicleNo"))).click()
    
    try:
        data["vehicleType"] = browser.find_element_by_xpath(locaters.selectVehicleType).text
    except:
        data["vehicleType"] = browser.find_element_by_xpath(locaters.selectVehicleType).text
    
    (vehicleUnloadingWeight, previousLRId) = getDifferentialDieselQuantity(browser.find_elements_by_xpath(locaters.selectLRIdList))
    
    mappingData = getMappingData(data, location)
    
    if(mappingData == []):
        log("Error","Vehicle + route wise mapping could not find a match for : " +  str(data))
        raise Exception("Vehicle + route wise mapping could not find a match for : " +  str(data))

    data["remark"] = remarkForDieselSlip
    
    
    if(vehicleUnloadingWeight > float(mappingData[3]) and previousLRId != data.get("LRId")):
        currentLR = data.get("LRId")
        try:
            data["LRId"] = previousLRId
            extraWeight = vehicleUnloadingWeight - float(mappingData[3])
            extraDieselQuantity = extraWeight * float(mappingData[4])
            if(round(extraDieselQuantity,2)>extraDieselQuantity):
                extraDieselQuantity -= 0.01
            extraDieselQuantity = round(extraDieselQuantity,2)
            data["qty"] = str(extraDieselQuantity)
            data["onAccountOf"] = onAccountForDeffrencialDiesel
            data["pumpname"] = mappingData[7]
            fill(browser, data)
        except Exception as e:
            log("ERROR",str(e))
            sendEmail(errorEmailTo,"Error generating differncial diesel",str(e))
        data["LRId"] = currentLR

    data["onAccountOf"] = onAccountForDieselDefault
    for i in range (0,mappingData[6]):
        data["pumpname"] = mappingData[7 + i + i]
        try:
            if("," in data["pumpname"]):
                data["pumpname"] = data.get("pumpname").split(",")[random.randint(0,len((data.get("pumpname").split(",")))-1)]
        except Exception as e:
            log("ERROR", str(e))

        data["qty"] = mappingData[8 + i + i]
        fill(browser, data)

    log("info", "END of generateDieselSlip.")
    


def fill(browser,data):
    
    log("info", "start of fill function (%s,%s)"%(str(browser),str(data)))

    browser.find_element_by_xpath(locaters.selectVehicleNo.replace("<VEHICLENO>",data.get("vehicleNo"))).click()
    try:
        elements = browser.find_elements_by_xpath(locaters.selectLRId)
    except:
        elements = browser.find_elements_by_xpath(locaters.selectLRId)
    for element in elements:
        if data.get("LRId") in element.text:
            element.click()
            break
    try:
        browser.find_element_by_xpath(locaters.selectPumpname.replace("<PUMPNAME>",data.get("pumpname"))).click()
    except:
        browser.find_element_by_xpath(locaters.selectPumpname.replace("<PUMPNAME>",data.get("pumpname"))).click()
    browser.find_element_by_id(locaters.inputRemark).send_keys(data.get("remark"))
    browser.find_element_by_xpath(locaters.selectOnAccountOf.replace("<ONACCOUNTOF>",data.get("onAccountOf"))).click()
    
    browser.find_element_by_id(locaters.inputQty).send_keys(data.get("qty"))
    browser.find_element_by_id(locaters.buttonAdd).click()

    try:
        WebDriverWait(browser, 3).until(expected_conditions.alert_is_present(),"waiting for alert message")
        alert = browser.switch_to.alert
        alertText = alert.text 
        alert.accept()
        log("info","alert accepted : "+ alertText)
        raise Exception(alertText)
    except TimeoutException:
        log("info", "no alert")
    
    browser.find_element_by_id(locaters.buttonSave).click()

    if("Saved Successfully" in browser.find_element_by_id(locaters.statusForDieselSlip).text):
        log("info",browser.find_element_by_id(locaters.statusForDieselSlip).text)

    log("info","END of fill function")

def getDifferentialDieselQuantity(LRIdList):

    log("info", "differencial diesel start")
    weight = 0
    previousRecord = ""
    i = 1
    if(len(LRIdList)>2):
        weight = float(re.search("Weight:-([0-9]+[\.]*[0-9]*)",LRIdList[2].text).group(1))
        previousRecord = LRIdList[2].text
    
    return (weight,previousRecord)

def getMappingData(data,location):
    
    log("info", "get mapping data: %s"%str((data)))
    db = xl.readxl(mappingSheetPath,ws=(location))
    records = db.ws(location).rows

    route = data.get("fromStation") + "-" + data.get("toStation")
    mappingData = []
    for record in records:
        if((data.get("vehicleType") in record[2]) and (route == record[0] or route == record[1])):
            mappingData = record
            if(mappingData[3] == "-"):
                mappingData[3] = "0"
                mappingData[4] = "0"
            break
    
    return mappingData




