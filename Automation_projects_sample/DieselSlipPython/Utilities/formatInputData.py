
def generateMap():
    file = open("E:\\tanushree\\MarketLR\\dataSmaple",mode='r')
    data = file.read()
    file.close()
    data = data.split("\n")
    key = data[0].split("|")
    value = data[1].split("|")
    print(dict(zip(key,value)))
    return dict(zip(key,value))

