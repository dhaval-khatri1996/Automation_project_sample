from config import notMarketLRVehicleList
import pylightxl as xl
from Utilities.logger import log

def isMarketLR(vehicleNo):
    log("info", "checking if is market vehicle : %s"%vehicleNo)
    db = xl.readxl(notMarketLRVehicleList,ws=("Sheet1"))
    vehicleList = db.ws("Sheet1").col(1)
    for vehicle in vehicleList:
        if(vehicleNo == vehicle):
            return False
    
    return True
    